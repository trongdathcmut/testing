import unittest
from dataclasses import replace
import numpy as np
from model import Config, solve, channel, intersects, BS, USERS, SURFACE, elements

class PhysicsTests(unittest.TestCase):
    def setUp(self):
        self.c = Config()

    def test_blockage_geometry(self):
        self.assertTrue(intersects(BS, USERS['R']))
        self.assertTrue(intersects(BS, USERS['T']))
        self.assertFalse(intersects(BS, SURFACE))
        for p in elements(replace(self.c, n=1024, fc_ghz=1)):
            self.assertFalse(intersects(BS, p))
            for ue in USERS.values():
                self.assertFalse(intersects(p, ue))

    def test_blockage_loss_is_power_db(self):
        for ue in USERS.values():
            a=channel(BS, ue, self.c)
            b=channel(BS, ue, replace(self.c, obstacle=False))
            self.assertAlmostEqual(20*np.log10(abs(b/a)),40)

    def test_ris_cannot_serve_transmission_side(self):
        row=solve(replace(self.c, mode='RIS'))['T']
        self.assertAlmostEqual(row['gain_db'],0)

    def test_zero_efficiency_equals_direct(self):
        for mode in ['RIS','ES','MS','TS']:
            for row in solve(replace(self.c, mode=mode, efficiency=0)).values():
                self.assertAlmostEqual(row['gain_db'],0)

    def test_es_conserves_allocated_power(self):
        r=solve(self.c,True)
        np.testing.assert_allclose(np.square(r['R']['weights'])+np.square(r['T']['weights']),1)

    def test_ms_partition_exact(self):
        r=solve(replace(self.c, mode='MS',n=17,split=.3),True)
        self.assertEqual(sum(r['R']['weights']),5)
        np.testing.assert_array_equal(np.array(r['R']['weights'])+r['T']['weights'],np.ones(17))

    def test_es_endpoint_equals_ris(self):
        a=solve(replace(self.c, mode='ES',split=1))
        b=solve(replace(self.c, mode='RIS'))
        for s in ['R','T']:
            self.assertAlmostEqual(a[s]['power_dbm'],b[s]['power_dbm'])

    def test_ts_averages_watts_not_dbm(self):
        r=solve(replace(self.c,mode='TS',split=.3))
        for s in ['R','T']:
            d=r[s]
            expected=d['duty']*10**((d['active_dbm']-30)/10)+(1-d['duty'])*10**((d['direct_dbm']-30)/10)
            self.assertAlmostEqual(d['power_w']/expected,1)

    def test_phase_alignment_triangle_bound(self):
        r=solve(self.c,True)
        for d in r.values():
            before=np.array(d['before_re'])+1j*np.array(d['before_im'])
            hd=complex(d['hd_re'],d['hd_im'])
            expected=10**((self.c.pt_dbm-30)/10)*(abs(hd)+np.abs(before).sum())**2
            self.assertAlmostEqual(d['power_w']/expected,1,places=10)

    def test_random_repeatable_and_continuous_best(self):
        a=solve(replace(self.c,phase='random'))
        self.assertEqual(a,solve(replace(self.c,phase='random')))
        ideal=solve(self.c)
        for s in ['R','T']:
            self.assertGreaterEqual(ideal[s]['power_w'],a[s]['power_w'])

    def test_quantization(self):
        r=solve(replace(self.c,bits=2),True)
        for d in r.values():
            np.testing.assert_allclose(np.mod(d['phi_deg'],90),0,atol=1e-9)

    def test_pt_scaling_and_input_bounds(self):
        a=solve(self.c);b=solve(replace(self.c,pt_dbm=33))
        for s in a:self.assertAlmostEqual(b[s]['power_dbm']-a[s]['power_dbm'],3)
        for bad in [{'n':0},{'n':3.2},{'split':2},{'fc_ghz':float('nan')},{'mode':'BAD'},{'obstacle':1},{'bits':True}]:
            with self.assertRaises(ValueError):Config.parse(bad)

if __name__=='__main__':unittest.main()
