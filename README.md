# RIS / STAR-RIS 

## Chạy trên Windows / VS Code

Yêu cầu:

- Python 3.10 trở lên
- Visual Studio Code
- Kết nối Internet khi cài thư viện lần đầu

Mở thư mục project bằng VS Code.

Chọn:

```text
Terminal → New Terminal
```

Sau đó chạy:

```powershell
python -m venv .venv
```

Cài thư viện:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Chạy chương trình:

```powershell
.venv\Scripts\python.exe app.py
```

Sau khi Terminal hiện địa chỉ:

```text
http://127.0.0.1:8000
```

mở địa chỉ này bằng Chrome hoặc Edge.

Giữ Terminal mở trong khi sử dụng chương trình.

Để dừng chương trình, nhấn:

```text
Ctrl + C
```

Không mở trực tiếp file:

```text
static/index.html
```

vì giao diện cần kết nối với Python server để thực hiện mô phỏng.

---

## Nếu lệnh `python` không hoạt động

Thử:

```powershell
py -3 -m venv .venv
```

Sau đó tiếp tục:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

---

## Nếu cổng 8000 đang được sử dụng

Chạy:

```powershell
.venv\Scripts\python.exe app.py --port 8080
```

Sau đó mở:

```text
http://127.0.0.1:8080
```
