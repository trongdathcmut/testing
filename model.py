"""Narrowband SISO RIS / ideal independent-phase STAR-RIS educational model.
All powers computed in W; dBm only at presentation. See docs/MODEL.md.
"""
from dataclasses import dataclass, asdict, replace
import math
import numpy as np

C = 299792458.0
BS = np.array([0., 0., 8.])
SURFACE = np.array([60., 20., 5.])
USERS = {'R': np.array([40., -10., 1.5]), 'T': np.array([90., -10., 1.5])}
WALL_MIN = np.array([18., -12., 0.])
WALL_MAX = np.array([24., 5., 14.])

@dataclass(frozen=True)
class Config:
    n: int = 256
    fc_ghz: float = 3.0
    pt_dbm: float = 30.0
    bs_gain_dbi: float = 10.0
    blockage_db: float = 40.0
    obstacle: bool = True
    efficiency: float = 0.9
    split: float = 0.5  # reflection power fraction / element fraction / time fraction
    mode: str = 'ES'
    phase: str = 'optimized'
    bits: int = 0  # 0 = continuous
    seed: int = 42

    @classmethod
    def parse(cls, data):
        if not isinstance(data, dict):
            raise ValueError('Cấu hình phải là một JSON object.')
        unknown = set(data) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError('Tham số không hợp lệ: ' + ', '.join(sorted(unknown)))
        c = cls(**data)
        for name, lo, hi in [('n', 1, 1024), ('fc_ghz', 1, 6), ('pt_dbm', -10, 40),
                             ('bs_gain_dbi', 0, 20), ('blockage_db', 0, 80),
                             ('efficiency', 0, 1), ('split', 0, 1), ('bits', 0, 4),
                             ('seed', 0, 2147483647)]:
            v = getattr(c, name)
            if isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) or not lo <= v <= hi:
                raise ValueError(f'{name} phải nằm trong [{lo}, {hi}].')
        for name in ['n', 'bits', 'seed']:
            if not isinstance(getattr(c, name), int):
                raise ValueError(f'{name} phải là số nguyên.')
        if not isinstance(c.obstacle, bool) or c.mode not in ['NONE', 'RIS', 'ES', 'MS', 'TS'] or c.phase not in ['optimized', 'random', 'zero']:
            raise ValueError('Chế độ mô phỏng không hợp lệ.')
        return c


def intersects(a, b):
    """Segment/AABB slab test; obstacle is checked for each physical link."""
    delta = b - a
    low, high = 0., 1.
    for i in range(3):
        if abs(delta[i]) < 1e-12:
            if a[i] < WALL_MIN[i] or a[i] > WALL_MAX[i]:
                return False
        else:
            t0, t1 = sorted(((WALL_MIN[i]-a[i])/delta[i], (WALL_MAX[i]-a[i])/delta[i]))
            low, high = max(low, t0), min(high, t1)
            if low > high:
                return False
    return True


def channel(a, b, c):
    distance = float(np.linalg.norm(b-a))
    wavelength = C/(c.fc_ghz*1e9)
    blocked = c.obstacle and intersects(a, b)
    attenuation = 10**(-c.blockage_db/20) if blocked else 1.
    return wavelength/(4*np.pi*distance)*attenuation*np.exp(-2j*np.pi*distance/wavelength)


def elements(c):
    cols = math.ceil(math.sqrt(c.n))
    rows = math.ceil(c.n/cols)
    spacing = C/(c.fc_ghz*1e9)/2
    indices = np.arange(c.n)
    return SURFACE + np.column_stack((np.zeros(c.n),
                                      (indices % cols-(cols-1)/2)*spacing,
                                      (indices // cols-(rows-1)/2)*spacing))


def dbm(power):
    return None if power <= 0 else float(10*np.log10(power)+30)


def solve(c, detail=False):
    pts = elements(c)
    gain = 10**(c.bs_gain_dbi/20)  # BS antenna field gain, used once per path
    pt = 10**((c.pt_dbm-30)/10)
    incoming = np.array([channel(BS, p, c) for p in pts])
    rng = np.random.default_rng(c.seed)
    random_phases = rng.uniform(0, 2*np.pi, (2, c.n))
    output = {}
    for ui, (side, ue) in enumerate(USERS.items()):
        hd = gain*channel(BS, ue, c)
        cascade = gain*incoming*np.array([channel(p, ue, c) for p in pts])
        phi = np.mod(np.angle(hd)-np.angle(cascade), 2*np.pi)
        if c.phase == 'random':
            phi = random_phases[ui]
        elif c.phase == 'zero':
            phi = np.zeros(c.n)
        if c.bits:
            step = 2*np.pi/(2**c.bits)
            phi = np.mod(np.round(phi/step)*step, 2*np.pi)
        weights = np.ones(c.n)
        duty = 1.
        if c.mode == 'NONE' or (c.mode == 'RIS' and side == 'T'):
            weights *= 0
        elif c.mode == 'ES':
            weights *= np.sqrt(c.split if side == 'R' else 1-c.split)
        elif c.mode == 'MS':
            count = int(np.floor(c.n*c.split+0.5))
            weights = (np.arange(c.n) < count if side == 'R' else np.arange(c.n) >= count).astype(float)
        elif c.mode == 'TS':
            duty = c.split if side == 'R' else 1-c.split
        before = np.sqrt(c.efficiency)*weights*cascade
        after = before*np.exp(1j*phi)
        hr = np.sum(after)
        p_direct = pt*abs(hd)**2
        p_active = pt*abs(hd+hr)**2
        p_average = duty*p_active+(1-duty)*p_direct
        row = dict(power_w=float(p_average), power_dbm=dbm(p_average),
                   direct_dbm=dbm(p_direct), active_dbm=dbm(p_active),
                   surface_only_dbm=dbm(pt*abs(hr)**2), duty=float(duty),
                   gain_db=float(10*np.log10(p_average/p_direct)),
                   direct_blocked=bool(c.obstacle and intersects(BS, ue)),
                   direct_distance_m=float(np.linalg.norm(BS-ue)))
        if detail:
            row.update(phi_deg=np.rad2deg(phi).tolist(), weights=weights.tolist(),
                       before_re=before.real.tolist(), before_im=before.imag.tolist(),
                       after_re=after.real.tolist(), after_im=after.imag.tolist(),
                       hd_re=float(hd.real), hd_im=float(hd.imag),
                       hr_re=float(hr.real), hr_im=float(hr.imag))
        output[side] = row
    return output


def simulate(c):
    selected = solve(c, True)
    cases = [('LOS', replace(c, mode='NONE', obstacle=False)),
             ('DIRECT', replace(c, mode='NONE')),
             ('RIS', replace(c, mode='RIS')),
             ('ES', replace(c, mode='ES')),
             ('MS', replace(c, mode='MS')),
             ('TS', replace(c, mode='TS'))]
    comparison = [dict(case=name, **solve(case)) for name, case in cases]
    ns = sorted(set([1, 4, 16, 32, 64, 128, 256, 512, 1024, c.n]))
    sweep = [dict(n=n, **solve(replace(c, n=n))) for n in ns]
    return dict(config=asdict(c), selected=selected, comparison=comparison, sweep=sweep,
                geometry=dict(bs=BS.tolist(), surface=SURFACE.tolist(),
                              users={k:v.tolist() for k,v in USERS.items()},
                              wall_min=WALL_MIN.tolist(), wall_max=WALL_MAX.tolist()),
                wavelength_m=C/(c.fc_ghz*1e9))
