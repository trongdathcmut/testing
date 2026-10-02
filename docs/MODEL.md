# Mô hình toán và giả thiết

## 1. Mục tiêu và hệ thống

Mô phỏng công suất thu của một tín hiệu chung từ BS tới hai UE, với và không có vật cản, trước và sau khi dùng RIS/STAR-RIS. Hệ thống SISO băng hẹp, kênh xác định theo hình học. Không mô phỏng hai luồng dữ liệu độc lập, NOMA, nhiễu đa người dùng, SINR, mã hóa hay throughput.

| Đối tượng | Tọa độ (x, y, z), mét |
|---|---|
| BS | (0, 0, 8) |
| Tâm bề mặt | (60, 20, 5) |
| UE-R | (40, -10, 1.5) |
| UE-T | (90, -10, 1.5) |
| Góc nhỏ vật cản | (18, -12, 0) |
| Góc lớn vật cản | (24, 5, 14) |

Bề mặt nằm trên mặt phẳng x = 60. BS và UE-R có x < 60, UE-T có x > 60. Vật cản là khối hộp chữ nhật. Hàm `intersects` kiểm tra giao giữa đoạn thẳng và hộp bằng thuật toán slab. Mỗi đoạn xuyên hộp chịu một lần suy hao L dB, không phụ thuộc chiều dài đi trong hộp. Đây là mô hình suy hao vật cản đơn giản; không có nhiễu xạ hoặc phản xạ từ tường.

Chọn hình học này để đường BS→UE-R và BS→UE-T cắt vật cản, còn các tuyến BS→bề mặt→UE tránh được. Bộ kiểm thử kiểm tra cả các phần tử ở cấu hình bề mặt lớn nhất trong dải cho phép.

## 2. Bố trí phần tử

- c = 299 792 458 m/s; λ = c/fc; d = λ/2.
- n_col = ceil(sqrt(N)); n_row = ceil(N/n_col).
- Phần tử n, đánh số từ 0, có tọa độ:

$$\mathbf p_n=\mathbf p_S+\left(0,\left[n\bmod n_{col}-{n_{col}-1\over2}\right]d,\left[\lfloor n/n_{col}\rfloor-{n_{row}-1\over2}\right]d\right).$$

Nếu N không lấp đầy lưới chữ nhật, hàng cuối còn trống. Khi tăng N với fc cố định, khoảng cách phần tử giữ λ/2 và kích thước bề mặt tăng. Vì vậy không diễn giải quét N là tăng mật độ trong cùng một diện tích. Khi đổi fc, khoảng cách phần tử cũng đổi để luôn bằng λ/2; đây không phải quét tần số của một bề mặt chế tạo cố định.

Trong hình 3D, bề mặt được phóng đại thành khoảng 17 m và biểu tượng thiết bị cũng được phóng đại để quan sát. **Python luôn dùng tọa độ phần tử thực ở trên**, không dùng kích thước hiển thị. Tia động và chu kỳ TS được làm chậm để minh họa.

## 3. Kênh từng chặng

Với khoảng cách d_ab, hệ số kênh phức vô hướng là:

$$h_{ab}={\lambda\over4\pi d_{ab}}\exp\left(-j{2\pi d_{ab}\over\lambda}\right)\,10^{-L_{ab}/20}.$$

L_ab = L nếu đoạn ab cắt vật cản đang bật, ngược lại bằng 0. Bình phương biên độ cho suy hao công suất dạng Friis với gain đẳng hướng bằng 1. Hệ số 10^(-L/20) áp dụng cho biên độ, không phải 10^(-L/10).

BS có gain công suất G_B = 10^(G_B,dBi/10), mặc định 10 dBi; UE gain 0 dBi. Gain BS là hằng số cho mọi hướng trong mô hình này, không mô phỏng giản đồ bức xạ. Đặt:

$$h_{d,u}=\sqrt{G_B}h_{BS,u},\qquad a_{u,n}=\sqrt{G_B}h_{BS,n}h_{n,u}.$$

Gain BS được nhân đúng một lần trong mỗi đường truyền. Nhánh qua RIS có suy hao của **hai chặng**, không thay bằng một đường Friis với khoảng cách d1+d2. Mô hình này là mô hình kênh phần tử lý tưởng quen dùng cho bài tập RIS, không phải mô hình tán xạ điện từ đã hiệu chuẩn theo diện tích/giản đồ phần tử.

## 4. Dịch pha và công suất

$$h_{S,u}=\sum_{n=1}^{N}\sqrt{\eta}\,w_{u,n}a_{u,n}e^{j\phi_{u,n}},\quad h_{eff,u}=h_{d,u}+h_{S,u}.$$

η ∈ [0,1] là hiệu suất **công suất** của bề mặt; w = √β là hệ số chia **biên độ**. Với pha liên tục và biết kênh hoàn hảo:

$$\phi_{u,n}=[\arg(h_{d,u})-\arg(a_{u,n})]\bmod 2\pi.$$

Mỗi đóng góp qua bề mặt được căn pha với đường trực tiếp. Với pha ngẫu nhiên, lấy Uniform[0,2π) bằng NumPy default_rng(seed=42). Với pha 0, tất cả hệ số pha bằng 1. Pha được lượng tử về mức gần nhất nếu b > 0:

$$\Delta=2\pi/2^b,\quad\phi_q=\Delta\,\operatorname{round}(\phi/\Delta)\bmod2\pi.$$

Lượng tử hóa từng phần tử là giải pháp đơn giản, không tìm tối ưu tổ hợp toàn cục cho bộ pha rời rạc. Pha ngẫu nhiên được giữ tái lập trong cùng cấu hình. Khi đổi N, chuỗi của UE-T không nhất thiết là tiền tố của cấu hình cũ vì máy phát số ngẫu nhiên tạo mảng (2,N).

$$P_t[W]=10^{(P_t[dBm]-30)/10},\quad P_{r,u}[W]=P_t|h_{eff,u}|^2,$$
$$P_{r,u}[dBm]=10\log_{10}(P_{r,u}[W])+30.$$

Mọi phép cộng và lấy trung bình công suất thực hiện trong W. Nếu nhánh bề mặt bằng 0, `surface_only_dbm` được ghi null (tương ứng −∞ dBm); không gán một sàn công suất giả vào phép tính.

## 5. RIS và STAR-RIS

| Chế độ | w_R,n | w_T,n | Diễn giải |
|---|---|---|---|
| Không bề mặt | 0 | 0 | Chỉ còn đường trực tiếp |
| RIS | 1 | 0 | Tất cả phần tử phản xạ tới R |
| ES | √α | √(1−α) | Chia năng lượng tại mọi phần tử |
| MS | 1 hoặc 0 | 1−w_R,n | Mỗi phần tử chỉ R hoặc T |
| TS | 1 khi phục vụ R | 1 khi phục vụ T | Hai cấu hình luân phiên thời gian |

ES bảo đảm w_R² + w_T² = 1 trước khi tính hiệu suất η. MS dùng N_R = floor(Nα + 0.5); N_R phần tử đầu phục vụ R, còn lại phục vụ T. Với N lẻ, tỷ lệ phần tử thực không nhất thiết bằng α chính xác.

TS dành τ_R=α và τ_T=1−α. BS vẫn phát tín hiệu chung liên tục; khi bề mặt không phục vụ UE nào đó, UE ấy vẫn có đường trực tiếp:

$$\bar P_{r,u}=\tau_u P_t|h_{d,u}+h_{S,u}|^2+(1-\tau_u)P_t|h_{d,u}|^2.$$

Giao diện so sánh **công suất trung bình theo thời gian**. JSON còn có `active_dbm` là công suất trong khe được bề mặt phục vụ. Nếu τ=0, đó chỉ là giá trị giả định của khe hoạt động; khe này không xảy ra. Đây không phải phép tính thông lượng TDMA.

**Giả thiết STAR-RIS:** pha R/T điều khiển độc lập lý tưởng. Không áp đặt điều kiện ghép pha của phần tử thụ động lossless. Mô hình này phù hợp để minh họa nguyên lý chia tài nguyên, nhưng có thể lạc quan hơn phần cứng thụ động thực. Muốn mô phỏng phần cứng thực cần lựa chọn mô hình phần tử cụ thể và giải bài toán tối ưu pha ghép.

## 6. Độ cải thiện

$$\Delta P_u[dB]=10\log_{10}\left({P_{r,u}\over P_{direct,u}}\right)=P_{r,u}[dBm]-P_{direct,u}[dBm].$$

Mốc so sánh luôn dùng **cùng vật cản, Pt, gain, tần số và vị trí**, chỉ bỏ bề mặt. Khi tắt vật cản, mốc tự trở thành LOS. Cột LOS trên biểu đồ luôn tắt vật cản và bề mặt, dù cấu hình hiện hành thế nào.

Không ép số liệu để RIS luôn vượt LOS. Với pha liên tục tối ưu, mô hình căn toàn bộ nhánh bề mặt theo hd nên công suất không thấp hơn mốc trực tiếp. Với pha ngẫu nhiên/pha 0/lượng tử hóa, cộng triệt tiêu là có thể. STAR-RIS không nhất thiết tăng công suất ở R hơn RIS vì cần dành tài nguyên cho T.

## 7. Giới hạn

Chưa có: CSI sai số, kênh fading đa đường, phân cực, ghép tương hỗ, giản đồ phần tử, suy hao góc tới, mô hình diện tích hiệu dụng đầy đủ, băng rộng OFDM, Doppler, tốc độ dữ liệu, nhiễu nhiệt, SINR, tối ưu vị trí hay phần cứng điều khiển. Pha khoảng cách được tính theo tọa độ từng phần tử, nhưng điều đó **không biến mô hình thành bộ giải điện từ gần trường**. Không ngoại suy luật tăng công suất theo N đến N vô hạn.

## 8. Tài liệu tham khảo

1. E. Björnson, Ö. Özdogan, E. G. Larsson, “Reconfigurable Intelligent Surfaces: Three Myths and Two Critical Questions”, 2020. https://arxiv.org/abs/2006.03377 — nguyên lý RIS và thận trọng về suy hao/array gain.
2. X. Mu, Y. Liu, L. Guo, J. Lin, R. Schober, “Simultaneously Transmitting And Reflecting (STAR) RIS Aided Wireless Communications”, 2021. https://arxiv.org/abs/2104.01421 — ba giao thức ES/MS/TS. Source này không tái hiện bài toán tối ưu beamforming trong bài báo.
3. J. Xu et al., “Simultaneously Transmitting and Reflecting (STAR)-RISs: A Coupled Phase-Shift Model”, 2021. https://arxiv.org/abs/2110.02374 — khác biệt giữa giả thiết pha độc lập và pha ghép thực tế.
4. Tham khảo cách tổ chức trải nghiệm trực quan: https://interactive-transformer.vercel.app/#intro. Không sử dụng mã nguồn của trang này.
