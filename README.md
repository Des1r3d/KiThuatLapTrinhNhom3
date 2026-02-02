# Hệ thống Quản lý Kho Thuốc

## Mô tả
Ứng dụng quản lý kho thuốc được xây dựng bằng Python và PyQt6, hỗ trợ theo dõi tồn kho, cảnh báo hết hạn, và tìm kiếm thông minh.

## Yêu cầu hệ thống
- Python 3.9+
- PyQt6
- pandas
- thefuzz
- matplotlib

## Cài đặt

### 1. Tạo môi trường ảo
```bash
python -m venv venv
```

### 2. Kích hoạt môi trường ảo
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

## Cấu trúc thư mục
```
KiThuatLapTrinhNhom3/
├── src/              # Mã nguồn chính
├── data/             # Dữ liệu JSON
├── tests/            # Unit tests
├── assets/           # Tài nguyên (icons, styles)
├── docs/             # Tài liệu
├── requirements.txt  # Thư viện Python
└── README.md         # File này
```

## Chạy ứng dụng
```bash
python src/main.py
```

## Phát triển
Xem file `docs/tickets.md` để biết chi tiết về các ticket phát triển.
