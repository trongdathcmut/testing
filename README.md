# RIS / STAR-RIS Interactive Lab

**Tên đề tài đề xuất:** Mô phỏng và trực quan hóa ảnh hưởng của RIS và STAR-RIS đến công suất thu trong môi trường có vật cản bằng Python.

Ứng dụng chạy trên máy cá nhân, có mô hình không gian 3D xoay/zoom, biểu tượng BS dạng ăng-ten và UE dạng điện thoại, đường truyền chuyển động, bản đồ pha, cộng vector phức và biểu đồ công suất. Cách khám phá theo từng bước lấy cảm hứng từ https://interactive-transformer.vercel.app/#intro; mã và giao diện được viết riêng cho đề tài này.

**Python tính toàn bộ kết quả vật lý.** HTML/CSS/JavaScript hiển thị và xử lý tương tác. Không cần Node.js, không dùng CDN, không cần tài khoản hay API key. Cần Internet khi cài NumPy lần đầu; sau đó chạy offline. Đây là bản source chạy local để nộp và trình diễn, chưa cấu hình triển khai Vercel.

## 1. Chạy trên Windows / VS Code

Cài Python 3.10 trở lên (bản 64 bit), giải nén toàn bộ thư mục. Mở thư mục `RIS_STAR_RIS_Lab` trong VS Code, chọn Terminal → New Terminal. Chạy:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Mở **http://127.0.0.1:8000** bằng Chrome hoặc Edge. Giữ terminal mở trong khi sử dụng. Nhấn `Ctrl+C` trong terminal để dừng. Không mở trực tiếp `index.html` vì giao diện cần gọi Python để tính toán.

Có thể nhấp đúp `run_windows.bat` để tạo môi trường và chạy server. Nếu không có lệnh `py`, thay `py -3` bằng `python`. Nếu cổng 8000 đang được dùng:

```powershell
.venv\Scripts\python.exe app.py --port 8080
```

Sau đó mở http://127.0.0.1:8080. Nếu pip báo lỗi kết nối, kiểm tra mạng/proxy và chạy lại lệnh cài đặt. Không cần hạ chính sách PowerShell vì không dùng Activate.ps1.

## 2. Chạy trên macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

## 3. Các thí nghiệm trên giao diện

- Đổi số phần tử N từ 1 đến 1024; mỗi phần tử cách nhau λ/2.
- Bật/tắt vật cản; chỉnh suy hao xuyên vật cản từ 0 đến 80 dB.
- So sánh không bề mặt, RIS, STAR-RIS ES, MS và TS.
- Đổi pha: căn pha lý tưởng, ngẫu nhiên có seed cố định, hoặc pha 0°.
- Chọn lượng tử pha liên tục hoặc 1–4 bit.
- Điều chỉnh tỷ lệ R/T, tần số, công suất phát, hiệu suất bề mặt.
- Chọn UE-R/UE-T để xem bản đồ pha; bấm từng ô để xem giá trị.
- Kéo mô hình để xoay, cuộn để zoom, chuyển góc nhìn trên.
- `Xuất kết quả`: tải JSON chứa cấu hình, công suất, pha, hệ số phức, hình học và dữ liệu quét N.
- `Lưu hình`: tải hình mô hình đang hiển thị dưới dạng PNG.

Các nút bước 01–05 thay phần giải thích, không tự thay các thông số thí nghiệm. Điều này giúp giữ nguyên cấu hình khi thuyết trình. Các thao tác điều khiển sẽ tự tính lại.

## 4. Cấu trúc mã nguồn

| File | Vai trò |
|---|---|
| `model.py` | Config, hình học, kiểm tra vật cản, kênh phức, pha, giao thức RIS/STAR-RIS, công suất |
| `app.py` | HTTP server localhost và API `POST /api/simulate` |
| `static/index.html` | Các điều khiển và nội dung hướng dẫn |
| `static/style.css` | Giao diện responsive |
| `static/app.js` | Chiếu mô hình 3D lên Canvas, tương tác, biểu đồ, gọi Python API |
| `experiments.py` | Chạy bộ thí nghiệm tái lập không cần giao diện |
| `tests/test_model.py` | Kiểm tra các tính chất vật lý và trường hợp biên |
| `docs/MODEL.md` | Công thức, tham số và giới hạn mô hình |
| `docs/REPORT_GUIDE.md` | Dàn ý báo cáo và kịch bản trình diễn |
| `results/` | JSON/CSV mẫu được sinh từ Python |

## 5. Xuất dữ liệu báo cáo

Tại thư mục dự án, dùng Python của môi trường ảo:

```powershell
.venv\Scripts\python.exe experiments.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS/Linux dùng `.venv/bin/python` thay cho `.venv\Scripts\python.exe`. Có thể dùng `python experiments.py --n 512 --output ket_qua_512` nếu đã kích hoạt môi trường ảo.

Các file CSV mở được bằng Excel. Cột `power_dbm` là công suất tuyệt đối; `gain_db` là mức cải thiện so với chỉ có đường trực tiếp trong cùng môi trường. Dữ liệu JSON chứa đầy đủ tham số mặc định để tái lập. Mẫu pha ngẫu nhiên là một lần thử với seed 42, không phải kết quả trung bình Monte Carlo.

## 6. Kết quả mặc định đã tái lập

N = 256, fc = 3 GHz, Pt = 30 dBm, gain BS = 10 dBi, suy hao vật cản = 40 dB, η = 0.9, tỷ lệ R = 0.5, pha liên tục được căn chỉnh.

| Trường hợp | UE-R (dBm) | UE-T (dBm) |
|---|---:|---:|
| LOS, không vật cản và không bề mặt | -34.40 | -41.15 |
| Có vật cản, không bề mặt | -74.40 | -81.15 |
| RIS | -61.31 | -81.15 |
| STAR-RIS ES | -63.56 | -66.19 |
| STAR-RIS MS | -65.59 | -68.58 |
| STAR-RIS TS, trung bình theo thời gian | -64.11 | -66.58 |

RIS không phục vụ phía T. STAR-RIS phân phối tài nguyên cho cả hai phía nên công suất phía R có thể thấp hơn RIS chỉ tập trung vào R. Tuyến qua bề mặt vẫn chịu suy hao hai chặng nên không tự động vượt LOS.

## 7. Phạm vi và ghi nhận

Đây là **mô phỏng kênh vô hướng SISO băng hẹp phục vụ học tập**, không phải phần mềm thiết kế phần tử siêu bề mặt/điện từ toàn sóng. STAR-RIS sử dụng pha R/T độc lập lý tưởng. Không gán kết quả này thành kết quả thực nghiệm hoặc kết quả phần cứng thụ động đã chế tạo. Đọc `docs/MODEL.md` trước khi viết phần nhận xét.

Source không sử dụng mã hoặc tài sản hình ảnh của trang mẫu. Phần cài đặt hiển thị và biểu tượng sơ đồ được viết riêng; NumPy là phụ thuộc bên ngoài và giữ giấy phép riêng của dự án NumPy.
