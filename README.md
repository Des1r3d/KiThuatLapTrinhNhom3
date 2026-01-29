PharmacyManager/
├── main.py                # Entry point: Khởi chạy ứng dụng chính
├── config.py              # Cấu hình hệ thống (Đường dẫn file, hằng số, Stylesheet)
├── requirements.txt       # Danh sách các thư viện cần cài đặt (PyQt6, pandas,...)
├── README.md              # Tài liệu hướng dẫn dự án
│
├── data/                  # Quản lý cơ sở dữ liệu
│   └── database.json      # File lưu trữ thông tin thuốc, tồn kho, giao dịch
│
├── src/                   # Mã nguồn chính của ứng dụng
│   ├── __init__.py
│   ├── ui/                # Giao diện người dùng (PyQt6)
│   │   ├── main_window.py # Giao diện chính của app
│   │   ├── dashboard.py   # Widget hiển thị Dashboard & Biểu đồ
│   │   └── resources/     # Chứa Icons, Hình ảnh, CSS (.qss)
│   │
│   ├── logic/             # Xử lý nghiệp vụ (Business Logic)
│   │   ├── inventory.py   # Quản lý nhập/xuất, vị trí kệ (Shelf/Bin)
│   │   ├── pricing.py     # Kiểm tra giá, tính toán doanh thu
│   │   └── expiry.py      # Thuật toán lọc & cảnh báo hạn sử dụng
│   │
│   └── utils/             # Các module bổ trợ (Helper functions)
│       ├── data_handler.py # Đọc/Ghi dữ liệu JSON bằng Pandas
│       └── plotter.py      # Cấu hình vẽ biểu đồ Matplotlib để nhúng vào UI
└── ...
