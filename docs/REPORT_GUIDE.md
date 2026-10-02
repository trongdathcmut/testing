# Hướng dẫn báo cáo và trình diễn

## Tên đề tài

**Mô phỏng và trực quan hóa ảnh hưởng của RIS và STAR-RIS đến công suất thu trong môi trường có vật cản bằng Python.**

## Câu hỏi nghiên cứu

1. Vật cản làm giảm công suất thu bao nhiêu khi giữ nguyên cấu hình phát?
2. Căn pha RIS giúp khôi phục công suất phía phản xạ như thế nào?
3. STAR-RIS phục vụ người dùng ở cả hai phía bằng ES/MS/TS ra sao?
4. Số phần tử, độ phân giải pha và tỷ lệ chia R/T ảnh hưởng kết quả thế nào?

## Bố cục đề nghị

1. **Giới thiệu:** bài toán vùng bị che khuất; mục tiêu; phạm vi mô hình học tập.
2. **Cơ sở lý thuyết:** hệ số kênh phức, công suất W/dBm, suy hao vật cản, RIS, STAR-RIS ES/MS/TS, căn pha.
3. **Mô hình hệ thống:** sơ đồ, bảng tọa độ, phương trình, tham số, giả thiết và giới hạn. Dùng `MODEL.md` làm cơ sở, diễn đạt lại theo cách hiểu của bạn.
4. **Thiết kế chương trình:** vai trò các file, luồng cấu hình → API → Python → kết quả → giao diện; giải thích `channel`, `solve`, `simulate`.
5. **Kết quả và nhận xét:** thực hiện các thí nghiệm dưới đây, chèn ảnh tự xuất, biểu đồ từ CSV, nêu giá trị định lượng.
6. **Kết luận:** lợi ích trong vùng che khuất; đánh đổi giữa hai phía; chưa xét pha ghép và kênh thực; hướng phát triển.
7. **Tài liệu tham khảo và phụ lục:** nguồn học thuật, hướng dẫn tái lập, source.

## Bộ thí nghiệm tối thiểu

| TN | Thay đổi | Giữ cố định | Kết quả cần ghi |
|---|---|---|---|
| 1 | Bật/tắt vật cản, không bề mặt | N=256, fc=3 GHz, Pt=30 dBm | Công suất giảm đúng 40 dB ở cả hai UE |
| 2 | Pha ngẫu nhiên → căn pha, mode RIS | Vật cản 40 dB, N=256 | Công suất R; T giữ nguyên; ảnh vector phức |
| 3 | N=16,64,256,512,1024 | Pha tối ưu, ES, α=0.5 | Công suất và độ cải thiện hai UE |
| 4 | RIS / ES / MS / TS | N=256, mọi tham số khác giống nhau | So sánh hai UE; TS dùng trung bình W |
| 5 | α=0,0.25,0.5,0.75,1 | ES, N=256 | Đánh đổi công suất R/T |
| 6 | Liên tục / 1 / 2 / 3 / 4 bit | ES, N=256 | Tổn thất do lượng tử hóa pha |

`experiments.py` có sẵn dữ liệu cho TN3, TN4, TN5 và quét suy hao vật cản. TN2 và TN6 có thể thao tác và xuất JSON trên giao diện. Không gọi một cấu hình pha ngẫu nhiên seed 42 là trung bình Monte Carlo. Nếu cần Monte Carlo, phải lặp nhiều seed, lấy trung bình công suất trong W và báo số lần thử/phân vị.

## Kịch bản thuyết trình khoảng 7–10 phút

- **Phút 0–1:** giới thiệu sơ đồ; chỉ BS, vật cản, bề mặt, UE-R/UE-T. Nhắc hai phía được xác định bởi mặt phẳng x=60.
- **Phút 1–2:** chọn không bề mặt; bật/tắt vật cản. Giải thích suy hao 40 dB tương đương giảm công suất 10.000 lần.
- **Phút 2–4:** bật RIS, chọn pha ngẫu nhiên rồi căn pha. Chỉ bản đồ pha và vector phức; giải thích tín hiệu cộng cùng pha.
- **Phút 4–5:** đổi N từ 64 lên 256, 512. Đọc dBm và ΔP; nhắc diện tích bề mặt đang tăng theo N.
- **Phút 5–7:** chuyển ES/MS/TS. Chỉ UE-T bắt đầu được hưởng đường truyền qua bề mặt; thay tỷ lệ R/T. Không so sánh công suất khe TS với công suất trung bình ES mà không nói rõ.
- **Phút 7–9:** xem biểu đồ tổng hợp, nêu kết luận và giới hạn; xuất JSON/hình để chứng minh khả năng tái lập.

## Các câu hỏi thường gặp

**Tại sao công suất có RIS vẫn thấp hơn LOS?** Tuyến qua bề mặt có suy hao hai chặng. Mục tiêu ở đây là cải thiện so với đường trực tiếp bị che, không phải chứng minh RIS luôn vượt LOS.

**Tại sao STAR-RIS ở R kém RIS?** RIS dành toàn bộ bề mặt để phản xạ cho R. STAR-RIS cần chia năng lượng, phần tử hoặc thời gian cho T.

**RIS có khuếch đại công suất không?** Không có bộ khuếch đại trong mô hình. Hiệu suất η ≤ 1. Định hướng và căn pha giúp năng lượng cộng kết hợp tại UE; tăng N cũng tăng diện tích thu/tán xạ. Mô hình đơn giản này không thay thế một phân tích cân bằng năng lượng toàn không gian.

**Giao diện có hoàn toàn bằng Python không?** Python tính toán mô phỏng. Trình duyệt dùng JavaScript Canvas để vẽ mô hình 3D và biểu đồ. Không tính lại công suất bằng JavaScript.

**Có mô phỏng sóng điện từ Maxwell không?** Không. Tia và phần tử là trực quan hóa của mô hình kênh băng hẹp, không phải bộ giải trường điện từ.

**Pha của STAR-RIS có thực hiện độc lập được không?** Đề tài này giả thiết điều khiển độc lập lý tưởng để phân tích nguyên lý. Phần tử thụ động thực có thể ràng buộc pha R/T; cần mô hình và tối ưu riêng.

## Khi nộp source

Nộp toàn bộ thư mục gồm source, README, docs, tests và results. Không cần nộp `.venv`, `__pycache__` hoặc các gói Python cài đặt. Trong báo cáo ghi phiên bản Python/NumPy thực tế trên máy bạn, tham số của từng thí nghiệm và phân biệt mô phỏng với đo thực nghiệm. Đọc và chạy từng chức năng trước khi bảo vệ.
