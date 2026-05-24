# ScholarScore - Phần Mềm Xét Điểm Học Bổng Sinh Viên

ScholarScore là một ứng dụng Python chuyên dụng giúp quản lý thông tin sinh viên, nhập điểm (Chuyên cần, Giữa kỳ, Cuối kỳ, Rèn luyện) và tự động tính toán, xét duyệt học bổng một cách trực quan, hiện đại.

## Tính năng nổi bật
1. **Giao diện 2 trong 1**: Hỗ trợ cả giao diện đồ hoạ (GUI) trực quan thân thiện và giao diện dòng lệnh (CLI) nhẹ nhàng.
2. **Quản lý Sinh viên**: Thêm, Sửa, Xoá, và Tìm kiếm linh hoạt với bộ lọc (Tất cả, MSV, Họ tên, Giới tính, SĐT).
3. **Nhập và Tính Điểm Tự Động**: Nhập điểm CC (10%), GK (30%), CK (60%) và điểm Rèn luyện. Hệ thống tự động tính điểm trung bình môn.
4. **Xét Học Bổng & Xếp Loại Tự Động**: 
   - Tự động xếp loại (Xuất sắc, Giỏi, Khá, Trung bình, Yếu) dựa trên điểm TB.
   - Tự động xét duyệt học bổng (Đủ điều kiện khi Điểm TB >= 8.0 VÀ Điểm Rèn luyện >= 80).
5. **Import/Export Dữ liệu**: Hỗ trợ nhập và xuất hàng loạt dữ liệu thông qua file `.csv`.

## Cấu trúc Dự án
```
ltpt-btl-20261-tt02b_nhom-2-main/
├── assets/                  # Icon và tài nguyên ảnh
├── controllers/             # Chứa logic điều khiển (gui_controller.py, cli_controller.py)
├── data/                    # Nơi lưu trữ database (hocbong.csv)
├── models/                  # Chứa logic tính toán và xử lý dữ liệu (tinhhocbong.py)
├── templates/               # Thư mục chứa biểu mẫu
├── utils/                   # Các tiện ích (Logger)
├── views/                   # Giao diện người dùng (gui_view.py, cli_view.py)
├── main.py                  # File khởi chạy ứng dụng chính (GUI/CLI)
├── main_cli.py              # File khởi chạy ứng dụng chính (chỉ CLI)
├── requirements.txt         # Khai báo các thư viện Python phụ thuộc cần cài đặt
├── README.md                # Tài liệu hướng dẫn chính, tổng quan về dự án
├── build.bat                # Script tự động đóng gói ứng dụng Python thành file thực thi (.exe)
├── clean.bat                # Script tự động dọn dẹp môi trường, xóa file rác, file tạm sau khi build
├── run_tests.bat            # Script tự động chạy toàn bộ các Unit Test của ứng dụng
└── setup_env.bat            # Script tự động tạo môi trường ảo (.venv) và cài đặt các thư viện cần thiết
```

## Hướng dẫn cài đặt và sử dụng dành cho Developer

### Thứ tự chạy các file Script (.bat)
Để hệ thống hoạt động trơn tru từ khi clone về máy, hãy chạy theo thứ tự sau:
1. Chạy **`setup_env.bat`**: Để tạo môi trường và tải thư viện.
2. Chạy **`main.py`** (thông qua lệnh python): Để chạy ứng dụng chính.
3. Chạy **`run_tests.bat`** (Tuỳ chọn): Để kiểm tra xem code có vượt qua các test cases không.
4. Chạy **`build.bat`** (Tuỳ chọn): Để xuất ra file `.exe` đem đi phân phối cho người dùng khác.
5. Chạy **`clean.bat`** (Tuỳ chọn): Dọn dẹp không gian đĩa nếu không cần thư mục build/dist nữa.

### 1. Khởi tạo môi trường
Bạn chỉ cần nhấp đúp chuột vào file `setup_env.bat` (trên Windows). 
Script này sẽ tự động:
- Tạo một môi trường ảo có tên là `.venv`.
- Kích hoạt môi trường ảo.
- Cài đặt toàn bộ thư viện cần thiết từ `requirements.txt` (như `pandas`, `numpy`, `pyinstaller`).

### 2. Chạy ứng dụng
Sau khi đã thiết lập môi trường, bạn có thể chạy phần mềm bằng lệnh:

**Chạy với Giao diện Đồ họa (GUI - Mặc định)**
```bash
.venv\Scripts\activate
python main.py
```

**Chạy với Giao diện Dòng lệnh (CLI - Terminal)**
Nếu bạn muốn sử dụng phần mềm trực tiếp trên môi trường dòng lệnh siêu nhẹ, hãy truyền thêm tham số `--cli`:
```bash
.venv\Scripts\activate
python main.py --cli
```

### 3. Đóng gói ra File Thực thi (.exe)
Để phân phối cho người dùng cuối (không cần cài đặt Python), hãy click đúp chuột vào file `build.bat`. 
Hệ thống sẽ dùng `PyInstaller` để biên dịch toàn bộ source code thành file `Setup_ScholarScore.exe` (Nếu bạn dùng thêm Inno Setup) hoặc bộ chạy độc lập trong thư mục `dist/`.

### 4. Dọn dẹp
Để lấy lại dung lượng bộ nhớ, bạn có thể chạy `clean.bat`. File này sẽ xóa các thư mục `build`, `dist` và các file cache của Python.

### 5. Cập nhật thư viện (Dependencies)
Trong quá trình phát triển, nếu bạn cài đặt thêm các thư viện mới, hãy chạy lệnh sau trong terminal (đã kích hoạt môi trường ảo `.venv`) để cập nhật lại file `requirements.txt`:
```bash
pip freeze > requirements.txt
```
