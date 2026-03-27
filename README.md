# 💊 PHARMA.SYS — Hệ Thống Quản Lý Kho Thuốc

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6.0+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ứng dụng desktop **quản lý kho thuốc** (Pharmacy Inventory Management) xây dựng bằng **Python + PyQt6**, hỗ trợ CRUD thuốc & kệ, cảnh báo thông minh, tìm kiếm mờ, và giao diện Light/Dark mode.

## ✨ Tính Năng Chính

### 📋 Quản Lý Kho

- ➕ **Thêm/Sửa/Xóa thuốc** với validation đầy đủ
- 🔍 **Tìm kiếm mờ** (fuzzy search) bằng TheFuzz
- 📊 **Dashboard** với biểu đồ thống kê Matplotlib
- 🗂️ **Quản lý kệ thuốc** với kiểm tra sức chứa
- 🖼️ **Ảnh thuốc** — lưu và hiển thị ảnh minh họa
- 🔢 **ID tự động** — định dạng `{shelf_id}.{seq:03d}` (VD: `K-A1.001`)

### ⚠️ Cảnh Báo Thông Minh

| Loại cảnh báo | Điều kiện | Mức độ |
|------------|-----------|--------|
| ❌ **Hết hạn** | `expiry_date <= today` | Cao |
| ⏰ **Sắp hết hạn** | Còn ≤ 30 ngày | Trung bình |
| 🚫 **Hết hàng** | `quantity == 0` | Cao |
| 📉 **Tồn kho thấp** | `quantity ≤ 5` và `> 0` | Thấp |

### 🎨 Giao Diện

- 🌞 **Light Mode** — Background: `#F4F6F8`, Surface: `#FFFFFF`
- 🌙 **Dark Mode** — Background: `#1F2933`, Surface: `#273947`
- 🔄 **Chuyển theme giữ nguyên trang** — không nhảy về Dashboard
- ⌨️ **Phím tắt** tiện lợi

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.13 hoặc cao hơn
- Windows 10/11, macOS, hoặc Linux

### Cài Đặt & Chạy

```bash
# Clone repository
git clone <repository-url>
cd KiThuatLapTrinhNhom3

# Cài đặt packages
pip install -r requirements.txt

# Chạy app
python app.py

# Hoặc dùng script Windows
run.bat
```

## 📖 Hướng Dẫn Sử Dụng

### Phím Tắt

| Phím Tắt | Chức Năng |
|----------|-----------|
| `Ctrl+K` | Mở tìm kiếm nhanh |
| `Ctrl+D` | Chuyển đổi Light/Dark mode |

### Thêm Thuốc Mới

1. Nhấn nút **"➕ Thêm thuốc mới"** trên trang Inventory
2. Điền các thông tin: Tên thuốc, Số lượng, Hạn sử dụng, Giá, Kệ thuốc
3. Nhấn **"Thêm thuốc"**

### Sửa/Xóa Thuốc

- **Xem chi tiết**: Double-click vào dòng thuốc
- **Sửa**: Chuột phải → "✏️ Sửa thuốc"
- **Xóa**: Chuột phải → "🗑️ Xóa thuốc"

### Tìm Kiếm

1. Nhấn `Ctrl+K` hoặc nút **"🔍 Tìm kiếm"**
2. Nhập tên thuốc (hỗ trợ fuzzy search, ngưỡng 70%)
3. Chọn kết quả để xem chi tiết

### Dashboard

Nhấn **"📊 Dashboard"** trên sidebar để xem:
- Tổng số thuốc, hết hạn, sắp hết hạn, tồn kho thấp (KPI)
- Biểu đồ tròn phân loại thuốc
- Top 10 thuốc theo tồn kho (biểu đồ cột)

## 📁 Cấu Trúc Dự Án

```
KiThuatLapTrinhNhom3/
├── app.py                      # 🚀 Điểm vào (QApplication setup)
├── requirements.txt            # Các phụ thuộc
├── run.bat                     # Script khởi chạy Windows
├── run_tests.bat               # Script chạy test
│
├── src/                        # 📦 Mã nguồn
│   ├── __init__.py             # Xuất package (Medicine, Shelf, v.v.)
│   ├── models.py               # Model dữ liệu: Medicine, Shelf
│   ├── storage.py              # StorageEngine: đọc/ghi JSON nguyên tử
│   ├── inventory_manager.py    # InventoryManager: CRUD, validate, sắp xếp
│   ├── alerts.py               # AlertSystem: cảnh báo hết hạn & tồn kho
│   ├── search_engine.py        # SearchEngine: tìm kiếm mờ
│   ├── image_manager.py        # ImageManager: ảnh thuốc
│   ├── dashboard_manager.py    # DashboardManager: xử lý dữ liệu dashboard
│   │
│   ├── views/                  # 📊 Các trang chính
│   │   ├── dashboard.py        # Giao diện dashboard (KPI + biểu đồ)
│   │   ├── inventory_view.py   # Bảng danh sách thuốc
│   │   └── shelf_view.py       # Trang quản lý kệ
│   │
│   ├── dialogs/                # 💬 Các hộp thoại
│   │   ├── medicine_dialog.py      # Thêm/Sửa thuốc
│   │   ├── shelf_dialog.py         # Thêm/Sửa kệ
│   │   ├── filter_dialog.py        # Lọc thuốc
│   │   ├── medicine_detail_view.py # Xem chi tiết thuốc
│   │   └── notification_dialogs.py # Thông báo thành công/lỗi/xác nhận
│   │
│   └── ui/                     # 🎨 Giao diện người dùng
│       ├── main_window.py       # MainWindow + SearchDialog (logic xử lý)
│       ├── theme/               # Hệ thống chủ đề (7 module)
│       │   ├── colors.py        # Bảng màu Light/Dark
│       │   ├── tokens.py        # Khoảng cách, bo góc, font chữ
│       │   ├── sidebar.py       # Hằng số sidebar
│       │   ├── cards.py         # Màu thẻ thống kê & biểu đồ
│       │   ├── core.py          # Lớp Theme, enum ThemeMode
│       │   ├── stylesheets.py   # Tạo stylesheet Qt
│       │   └── badges.py        # Hàm trợ giúp huy hiệu/cảnh báo
│       │
│       └── generated/           # ⚠️ TỰ ĐỘNG SINH — KHÔNG CHỈNH SỬA
│           ├── main_window_ui.py / main_window_ui_dark.py
│           ├── search.py / search_dark.py
│           ├── them_thuoc.py / them_thuoc_dark.py
│           ├── them_ke.py / them_ke_dark.py
│           ├── loc_thuoc.py / loc_thuoc_dark.py
│           └── ... (các dialog notification sáng + tối)
│
├── data/                       # 💾 Lưu trữ dữ liệu
│   ├── medicines.json          # CSDL thuốc
│   ├── shelves.json            # CSDL kệ
│   ├── settings.json           # Cài đặt (theme, ngưỡng)
│   └── images/                 # Ảnh thuốc
│
├── tests/                      # 🧪 Unit tests (~152 tests)
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_inventory.py
│   ├── test_alerts.py
│   ├── test_search.py
│   └── test_image_manager.py
│
├── docs/                       # 📚 Tài liệu
│   ├── classflow.md
│   ├── projectcharts.md
│   ├── design_guideline.md
│   └── classDiagram.drawio.png
│
├── design-ui/                  # 🎨 Tài sản thiết kế
│   └── design-ui/Qt_designer/  # File .ui & Logo.png
│
└── Ui Qt/                      # File .ui gốc Qt Designer (cặp Sáng + Tối)
    ├── main_window.ui / main_window_dark.ui
    ├── them_thuoc.ui / them_thuoc_dark.ui
    ├── them_ke.ui / them_ke_dark.ui
    ├── loc_thuoc.ui / loc_thuoc_dark.ui
    ├── search.ui / search_dark.ui
    └── ... (notification dialogs sáng + tối)
```

> ⚠️ **Không chỉnh sửa** files trong `src/ui/generated/` — chúng được sinh tự động bởi `pyuic6`.
> Sau khi sửa file `.ui`, chạy: `.venv/Scripts/pyuic6.exe "Ui Qt/<file>.ui" -o "src/ui/generated/<file>.py"`

## 🛠️ Công Nghệ

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3.13+ |
| UI Framework | PyQt6 ≥ 6.6.0 |
| Charts | Matplotlib ≥ 3.8.0 |
| Fuzzy Search | TheFuzz ≥ 0.22.0 + python-Levenshtein |
| UI Design | Qt Designer (.ui files) |
| Data Storage | JSON files (atomic writes) |
| Testing | pytest (~152 tests) |

## 📊 Kiến Trúc

| Pattern | Mô tả |
|---------|--------|
| **MVC** | Models (`models.py`) — Views (`views/`, `dialogs/`) — Controller (`inventory_manager.py`, `dashboard_manager.py`) |
| **Repository** | `StorageEngine` trừu tượng hóa file I/O |
| **Immutable Update** | `update_medicine()` tạo object mới thay vì mutate |
| **Atomic Write** | Ghi file qua temp → rename, có backup recovery |
| **Signal/Slot** | Hệ thống sự kiện Qt cho giao tiếp UI |
| **Observer** | Dashboard + InventoryView lắng nghe thay đổi data |
| **Dual UI** | Mỗi dialog có 2 generated files (sáng + tối), chọn tại runtime |

## 🧪 Testing

```bash
pytest tests/ -v
```

| File Test | Phạm vi |
|-----------|---------|
| `test_models.py` | Dataclass Medicine & Shelf, kiểm tra, chuyển đổi dữ liệu |
| `test_storage.py` | Ghi nguyên tử, sao lưu/phục hồi, xử lý file hỏng |
| `test_inventory.py` | Thao tác CRUD, tạo ID, kiểm tra sức chứa |
| `test_alerts.py` | Cảnh báo hết hạn/tồn kho, sắp xếp theo mức độ |
| `test_search.py` | Khớp mờ, ngưỡng, gợi ý |
| `test_image_manager.py` | CRUD ảnh, kiểm tra, đổi tên |

**Tổng: ~152 tests**

## 📝 Lưu Ý

### Giới Hạn Phiên Bản Beta

- ⚠️ Không có phân quyền người dùng
- 💾 Lưu trữ local (JSON), không có cloud sync
- 📈 Chưa tối ưu cho >10,000 bản ghi
- ↩️ Không có chức năng Undo

### Lưu Ý Kỹ Thuật

- **Phân tách module UI:** `views/` và `dialogs/` nằm ở `src/views/` và `src/dialogs/` (import: `from src.views.xxx` / `from src.dialogs.xxx`), **không phải** `src.ui.views`
- `src/ui/` chỉ chứa: `main_window.py`, `theme/`, `generated/`
- Logo nằm tại: `design-ui/design-ui/Qt_designer/Logo.png`
- Sidebar background (`#1C2944`) giữ nguyên cho cả Light và Dark mode
- Medicine ID tự động thay đổi khi chuyển kệ
- `Shelf.capacity` lưu kiểu `str` — cần cast `int` khi tính toán
- `StorageEngine` tự sao lưu trước khi ghi, tự phục hồi khi file bị hỏng

### Data Backup

Hệ thống tự động tạo backup khi lưu dữ liệu:
- `medicines.json.backup`
- `shelves.json.backup`

## 👥 Nhóm Phát Triển

**Môn:** Kỹ Thuật Lập Trình — Nhóm 3

## 📄 License

MIT License — xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 📞 Liên Hệ

Báo lỗi hoặc đề xuất tính năng mới qua Issues trên repository.

---

**Phiên bản:** 1.0.0 Beta  
**Ngày cập nhật:** 27/03/2026
