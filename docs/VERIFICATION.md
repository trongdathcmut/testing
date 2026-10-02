# Kiểm tra bàn giao

Môi trường thực hiện: Python 3.12.14, NumPy 2.3.5, Chrome headless 154 trên Linux. Script Windows được cung cấp để chạy trên máy người dùng; chưa chạy trực tiếp trên Windows trong phiên kiểm tra này.

## Kết quả

- 12 kiểm thử trong `tests/test_model.py` đạt.
- `experiments.py` chạy thành công, tạo dữ liệu JSON/CSV trong `results/`.
- Giao diện gọi Python thành công: cấu hình mặc định hiển thị R = −63.56 dBm, T = −66.19 dBm.
- Chuyển RIS: phía T giữ −81.15 dBm (không được bề mặt phục vụ).
- Tắt vật cản trong RIS: phía T tăng tới −41.15 dBm, đúng mốc LOS.
- Chuyển TS, pha ngẫu nhiên, 1024 phần tử: đủ 1024 ô pha và truy xuất được phần tử cuối.
- Tải JSON qua nút Xuất kết quả: file parse được, chứa cấu hình và đủ 256 pha sau khi đặt lại.
- Không ghi nhận lỗi JavaScript trong lượt kiểm tra tương tác.
- Ở viewport 390 × 844: không tràn trang theo chiều ngang; nhãn sơ đồ dùng bản rút gọn.
- Ảnh `preview.png` là ảnh giao diện thật đang chạy, không phải ảnh thiết kế giả lập.

Các kiểm thử kiểm chứng triển khai theo mô hình đã chọn, không chứng minh độ chính xác với phần cứng RIS ngoài thực tế.
