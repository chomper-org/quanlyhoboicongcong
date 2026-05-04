# Hướng dẫn cài đặt website Quản lý hồ bơi trên máy tính mới

> [!NOTE]
> Hệ thống được xây dựng bằng framework **Django (Python)** kết hợp với cơ sở dữ liệu **MySQL**. Dưới đây là các bước chi tiết để đưa mã nguồn này chạy thành công trên một máy tính Windows (hoặc Mac/Linux tương tự).

## 1. Yêu cầu hệ thống (Prerequisites)
Để hệ thống có thể chạy được, máy tính mới cần được cài đặt sẵn:
- **Python**: Phiên bản 3.8 trở lên (Khuyên dùng 3.10+). Nhớ tick chọn **"Add Python to PATH"** trong quá trình cài đặt.
- **MySQL Server**: Phiên bản 5.7 hoặc 8.0+. (Bạn có thể dùng ServBay, XAMPP, Laragon, hoặc cài đặt trực tiếp MySQL Server).
- **Git** (nếu bạn sử dụng Git để quản lý source code).

---

## 2. Các bước cài đặt chi tiết

### Bước 1: Tải mã nguồn về máy tính
1. Copy toàn bộ thư mục dự án (`quanlyhoboicongcong`) vào máy tính mới.
2. Hoặc nếu bạn dùng Git, hãy mở Terminal (PowerShell/CMD) và chạy lệnh:
   ```bash
   git clone <đường-dẫn-repo-của-bạn>
   cd quanlyhoboicongcong
   ```

### Bước 2: Thiết lập cơ sở dữ liệu (MySQL)
Mở công cụ quản lý MySQL của bạn (ví dụ: phpMyAdmin, DBeaver, MySQL Workbench, hoặc CLI) và thực hiện các bước sau:

1. **Tạo Database:** Tạo một database mới có tên là `poolweb` với charset là `utf8mb4`:
   ```sql
   CREATE DATABASE poolweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. **Kiểm tra thông tin đăng nhập:** Mở file `PoolManager/settings.py` (khoảng dòng 61). Nếu máy mới của bạn sử dụng tài khoản/mật khẩu MySQL khác, hãy cập nhật lại:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'poolweb',
           'USER': 'root',               # Thay bằng user MySQL máy mới nếu cần
           'PASSWORD': 'ServBay.dev',    # Thay bằng password MySQL máy mới nếu cần
           'HOST': '127.0.0.1',
           'PORT': '3306',
           # ...
       }
   }
   ```

### Bước 3: Thiết lập môi trường ảo (Virtual Environment)
Việc sử dụng môi trường ảo giúp tách biệt các thư viện của dự án này với các dự án khác trên máy. Mở Terminal/PowerShell tại thư mục gốc của dự án (`quanlyhoboicongcong`) và chạy:

**1. Tạo môi trường ảo (chỉ cần làm 1 lần):**
```powershell
python -m venv venv
```

**2. Kích hoạt môi trường ảo:**
- Trên **Windows** (PowerShell):
  ```powershell
  .\venv\Scripts\activate
  ```
- Trên **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```
*(Bạn sẽ thấy xuất hiện chữ `(venv)` ở đầu dòng lệnh, chứng tỏ môi trường ảo đã được kích hoạt).*

### Bước 4: Cài đặt các thư viện (Dependencies)
Đảm bảo bạn đang ở trong môi trường ảo, hãy chạy lệnh sau để cài đặt toàn bộ các thư viện mà dự án yêu cầu (như Django, mysqlclient,...):
```powershell
pip install -r requirements.txt
```
*(Lưu ý: Tôi đã tạo sẵn file `requirements.txt` trong thư mục dự án cho bạn).*

### Bước 5: Khởi tạo dữ liệu (Migration)
Sau khi đã thiết lập Database và cài đặt thư viện thành công, bạn cần đồng bộ hóa cấu trúc bảng của Django vào trong MySQL:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Bước 6: Tạo tài khoản Quản trị (Superuser)
Để có thể đăng nhập vào hệ thống Admin, bạn cần tạo một tài khoản quản trị cao nhất:
```powershell
python manage.py createsuperuser
```
> [!TIP]
> Hệ thống sẽ yêu cầu bạn nhập `Username`, `Email` (có thể bỏ qua) và `Password`. Lưu ý khi gõ mật khẩu, ký tự sẽ không hiển thị trên màn hình vì lý do bảo mật. Cứ gõ bình thường rồi nhấn Enter.

### Bước 7: Khởi chạy máy chủ Web (Run Server)
Bây giờ mọi thứ đã sẵn sàng. Hãy khởi chạy server Django:
```powershell
python manage.py runserver
```

Trang web của bạn đã hoạt động! Bạn có thể truy cập qua trình duyệt:
- **Trang chủ:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Trang Quản trị Admin:** [http://127.0.0.1:8000/admin-panel/login/](http://127.0.0.1:8000/admin-panel/login/)

---

## 3. Các lỗi thường gặp (Troubleshooting)

> [!WARNING]
> **Lỗi khi cài đặt `mysqlclient` qua lệnh pip**
> Trên Windows, máy mới thường thiếu bộ công cụ build C++. Nếu bị lỗi đỏ khi chạy `pip install -r requirements.txt`, bạn hãy tải và cài đặt [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), check chọn mục **"Desktop development with C++"** rồi tiến hành cài lại thư viện.

> [!WARNING]
> **Lỗi "Access denied for user"**
> Khi chạy `migrate` hoặc `runserver` mà thấy lỗi này, tức là thông tin Username hoặc Password của MySQL trong `PoolManager/settings.py` không khớp với MySQL trên máy mới. Bạn cần sửa lại cho đúng với thông tin tài khoản MySQL bạn đang dùng.
