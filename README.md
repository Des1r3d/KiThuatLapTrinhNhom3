# 💊 Hệ Thống Quản Lý Kho Thuốc

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hệ thống quản lý kho thuốc chuyên nghiệp với giao diện đồ họa PyQt6, hỗ trợ theo dõi hạn dùng, tồn kho và tìm kiếm thông minh.

## ✨ Tính Năng Chính

### 📋 Quản Lý Kho

- ➕ **Thêm/Sửa/Xóa thuốc** với validation đầy đủ
- 🔍 **Tìm kiếm mờ** (fuzzy search) thông minh
- 📊 **Bảng điều khiển** với biểu đồ thống kê
- 🗂️ **Tổ chức theo kệ** với vị trí cụ thể

### ⚠️ Cảnh Báo Thông Minh

- ❌ **Hết hạn**: Thuốc đã quá hạn sử dụng
- ⏰ **Sắp hết hạn**: Cảnh báo trước 30 ngày
- 📉 **Tồn kho thấp**: Dưới ngưỡng 5 đơn vị
- 🚫 **Hết hàng**: Số lượng = 0

### 🎨 Giao Diện

- 🌞 **Light Mode**: Giao diện sáng chuyên nghiệp
- 🌙 **Dark Mode**: Giao diện tối dịu mắt
- 🎨 **Màu sắc cảnh báo** trực quan
- ⌨️ **Phím tắt** tiện lợi

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.13 hoặc cao hơn
- Windows 10/11, macOS, hoặc Linux

### Cài Đặt Dependencies

```bash
# Clone repository
git clone <repository-url>
cd KiThuatLapTrinhNhom3

# Cài đặt packages
pip install -r requirements.txt
```

### Khởi Chạy Ứng Dụng

```bash
python app.py
```

## 📖 Hướng Dẫn Sử Dụng

### Phím Tắt

| Phím Tắt | Chức Năng |
|----------|-----------|
| `Ctrl+K` | Mở tìm kiếm nhanh |
| `Ctrl+N` | Thêm thuốc mới |
| `Ctrl+D` | Chuyển đổi Light/Dark mode |

### Thêm Thuốc Mới

1. Nhấn nút **"➕ Thêm thuốc mới"** hoặc `Ctrl+N`
2. Điền các thông tin:
   - Tên thuốc (bắt buộc)
   - Số lượng (≥ 0)
   - Hạn sử dụng
   - Giá (≥ 0)
   - Kệ thuốc
3. Nhấn **"Thêm thuốc"**

### Sửa/Xóa Thuốc

- **Sửa**: Double-click vào dòng thuốc hoặc chuột phải → "✏️ Sửa thuốc"
- **Xóa**: Chuột phải → "🗑️ Xóa thuốc"

### Tìm Kiếm

1. Nhấn `Ctrl+K` hoặc nút **"🔍 Tìm kiếm"**
2. Nhập tên thuốc (hỗ trợ tìm kiếm mờ)
3. Chọn kết quả để xem chi tiết

### Xem Dashboard

Nhấn **"📊 Bảng điều khiển"** trên sidebar để xem:

- Tổng số thuốc
- Số lượng đã hết hạn / sắp hết hạn
- Tồn kho thấp
- Biểu đồ phân bố
- Top 10 thuốc theo tồn kho

## 📁 Cấu Trúc Dự Án

```
KiThuatLapTrinhNhom3/
├── app.py                  # Entry point
├── src/
│   ├── models.py           # Data models (Medicine, Shelf)
│   ├── storage.py          # JSON storage engine
│   ├── inventory_manager.py # CRUD operations
│   ├── alerts.py           # Alert system
│   ├── search_engine.py    # Fuzzy search
│   └── ui/
│       ├── theme.py        # Theme system
│       ├── main_window.py  # Main window
│       ├── dashboard.py    # Dashboard view
│       ├── inventory_view.py # Table view
│       └── medicine_dialog.py # Add/Edit dialog
├── data/
│   ├── medicines.json      # Medicine database
│   └── shelves.json        # Shelf database
├── tests/                  # Unit tests
├── docs/                   # Documentation
└── requirements.txt        # Dependencies
```

## 🎨 Thiết Kế UI

Giao diện tuân theo **Design Guidelines**:

- **Màu sắc**: Calm & Professional
- **Typography**: Sans-serif, clean
- **Spacing**: Base unit 8px
- **Border Radius**: 8px
- **Contrast Ratio**: WCAG AA compliant

### Light Mode

- Background: `#F4F6F8`
- Primary: `#2E6F95`
- Surface: `#FFFFFF`

### Dark Mode

- Background: `#1F2933`
- Primary: `#4FA3D1`
- Surface: `#273947`

## 🧪 Testing

Chạy unit tests:

```bash
pytest tests/ -v
```

Độ phủ test hiện tại: **107 tests** covering models, storage, inventory, alerts, và search.

## 📊 Kiến Trúc

- **Repository Pattern**: `StorageEngine` abstract file operations
- **Immutable Patterns**: Dataclasses for data integrity
- **Atomic Operations**: Safe file writes with backup
- **MVC Pattern**: Separation of UI and business logic
- **Signal/Slot**: Qt event-driven architecture

## 🛠️ Công Nghệ

- **UI Framework**: PyQt6
- **Charts**: Matplotlib
- **Search**: TheFuzz (fuzzy string matching)
- **Data**: Pandas for data manipulation
- **Storage**: JSON with atomic writes

## 📝 Lưu Ý

### Giới Hạn Phiên Bản Beta

- ⚠️ Không có phân quyền người dùng
- 💾 Lưu trữ local (JSON), không có cloud sync
- 📈 Chưa tối ưu cho >10,000 bản ghi
- ↩️ Không có chức năng Undo
- 📊 Báo cáo cơ bản

### Data Backup

Hệ thống tự động tạo backup khi lưu dữ liệu:

- `medicines.json.backup`
- `shelves.json.backup`

### Xử Lý Lỗi

- File bị hỏng → Tự động khôi phục từ backup
- Validation errors → Hiển thị thông báo rõ ràng
- Empty data → Khởi tạo với dữ liệu mẫu

## 👥 Nhóm Phát Triển

**Môn:** Kỹ Thuật Lập Trình - Nhóm 3

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 📞 Liên Hệ

Báo lỗi hoặc đề xuất tính năng mới qua Issues trên repository.

---

**Phiên bản:** 1.0.0 Beta  
**Ngày cập nhật:** 14/02/2026
