##1. Sơ đồ cấu trúc thư mục (Project Structure)
PharmacyManager/
│
├── main.py                 # File chạy chính (Entry point)
├── config.py               # Các cấu hình chung (Đường dẫn file, màu sắc UI...)
│
├── data/                   # Nơi chứa dữ liệu
│   └── database.json       # File JSON lưu trữ thông tin
│
├── src/                    # Mã nguồn chính
│   ├── __init__.py
│   ├── ui/                 # Chuyên về giao diện (PyQt6)
│   │   ├── main_window.py  
│   │   ├── dashboard_ui.py # Code/File thiết kế Dashboard
│   │   └── resources/      # Icon, hình ảnh, stylesheet (qss)
│   │
│   ├── logic/              # Xử lý nghiệp vụ (Nối logic với UI)
│   │   ├── inventory.py    # Xử lý tồn kho, vị trí kệ
│   │   ├── pricing.py      # Kiểm tra lỗi nhập giá
│   │   └── expiry.py       # Kiểm tra hạn sử dụng
│   │
│   ├── utils/              # Các công cụ hỗ trợ
│   │   ├── data_handler.py # Đọc/Ghi file JSON bằng Pandas
│   │   └── plotter.py      # Vẽ biểu đồ Matplotlib
│   └── ...
│
├── requirements.txt        # Danh sách thư viện (PyQt6, pandas, matplotlib)
└── README.md               # Hướng dẫn sử dụng
