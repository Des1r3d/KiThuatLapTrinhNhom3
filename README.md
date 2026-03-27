#  PHARMA.SYS — Hệ Thống Quản Lý Kho Thuốc

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6.0+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ứng dụng desktop **quản lý kho thuốc** (Pharmacy Inventory Management) xây dựng bằng **Python + PyQt6**, hỗ trợ CRUD thuốc & kệ, cảnh báo thông minh, tìm kiếm mờ, và giao diện Light/Dark mode.

## Tính Năng Chính

### Quản Lý Kho

- **Thêm/Sửa/Xóa thuốc** với validation đầy đủ
- **Tìm kiếm mờ** (fuzzy search) bằng TheFuzz
-  **Dashboard** với biểu đồ thống kê Matplotlib
-  **Quản lý kệ thuốc** với kiểm tra sức chứa
-  **Ảnh thuốc** — lưu và hiển thị ảnh minh họa
-  **ID tự động** — định dạng `{shelf_id}.{seq:03d}` (VD: `K-A1.001`)

### ⚠️ Cảnh Báo Thông Minh

| Loại cảnh báo | Điều kiện | Mức độ |
|------------|-----------|--------|
| ❌ **Hết hạn** | `expiry_date <= today` | Cao |
| ⏰ **Sắp hết hạn** | Còn ≤ 30 ngày | Trung bình |
| 🚫 **Hết hàng** | `quantity == 0` | Cao |
| 📉 **Tồn kho thấp** | `quantity ≤ 5` và `> 0` | Thấp |

### Giao Diện

- 🌞 **Light Mode** — Background: `#F4F6F8`, Surface: `#FFFFFF`
- 🌙 **Dark Mode** — Background: `#1F2933`, Surface: `#273947`
- 🔄 **Chuyển theme giữ nguyên trang** — không nhảy về Dashboard
- ⌨️ **Phím tắt** tiện lợi

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

## Hướng Dẫn Sử Dụng

### Điều Hướng Chính

Ứng dụng có thanh sidebar cố định bên trái với ba trang chính:

| Trang | Mô tả |
|-------|-------|
| Dashboard | Tổng quan kho với KPI và biểu đồ thống kê |
| Danh sách thuốc | Bảng quản lý toàn bộ thuốc trong kho |
| Quản lý kệ | Bảng quản lý các kệ và sức chứa |

Nhấn vào tên trang trên sidebar để chuyển trang. Trang hiện tại sẽ được tô sáng.

---

### Dashboard

Trang Dashboard hiển thị tổng quan kho thuốc theo thời gian thực:

- **4 thẻ KPI**: Tổng thuốc, số thuốc đã hết hạn, số thuốc sắp hết hạn (trong vòng 30 ngày), số thuốc tồn kho thấp (so le 5 đơn vị).
- **Biểu đồ tròn**: Phân loại trạng thái tất cả thuốc trong kho.
- **Biểu đồ cột**: Top 10 thuốc theo số lượng tồn kho.
- **Bảng cảnh báo**: Danh sách thuốc sắp hết hạn và thuốc tồn kho thấp cần chú ý.

Dữ liệu Dashboard tự động cập nhật sau mỗi thao tác thêm, sửa, hoặc xóa thuốc.

---

### Quản Lý Thuốc (Danh Sách Thuốc)

#### Xem Danh Sách

Trang hiển thị bảng toàn bộ thuốc với các cột: Mã thuốc, Tên thuốc, Số lượng, Hạn sử dụng, Kệ, Giá, Trạng thái.

Màu sắc dòng trong bảng phản chiếu trạng thái:
- Màu đỏ: Hết hạn hoặc hết hàng
- Màu cam: Sắp hết hạn (trong 30 ngày)
- Màu vàng: Tồn kho thấp (so le 5 đơn vị, còn hàng)
- Không tô màu: Bình thường

Nhấn tiêu đề cột để sắp xếp. Nhãn phía trên bảng hiển thị tổng số mục (hoặc số mục sau lọc).

#### Xem Chi Tiết Thuốc

Double-click vào bất kỳ dòng nào trong bảng để mở cửa sổ chi tiết chỉ đọc của thuốc đó. Từ cửa sổ này có thể chuyển sang chỉnh sửa hoặc xóa.

#### Thêm Thuốc Mới

1. Nhấn nút **"Thêm thuốc mới"** phía trên bảng.
2. Điền đầy đủ thông tin trong hộp thoại:
   - Tên thuốc
   - Số lượng
   - Hạn sử dụng (chọn từ lịch)
   - Giá (VND)
   - Kệ thuốc (chọn từ danh sách kệ đã có)
   - Ảnh minh họa (tuỳ chọn — nhấn "Chọn ảnh" để tải lên)
3. Nhấn **"Thêm thuốc"** để xác nhận. Mã thuốc được tự động tạo theo định dạng `{shelf_id}.{seq:03d}` (ví dụ: `K-A1.001`).
4. Hộp thoại thông báo thành công xuất hiện với mã thuốc vừa tạo.

Lưu ý: Nếu kệ đã đầy, hệ thống hiện thông báo lỗi và không cho phép thêm thuốc vào kệ đó.

#### Sửa Thuốc

Có hai cách mở hộp thoại chỉnh sửa:

- **Cách 1**: Double-click vào dòng thuốc, sau đó nhấn nút "Sửa" trong cửa sổ chi tiết.
- **Cách 2**: Chuột phải vào dòng thuốc → chọn **"Chỉnh sửa thuốc"** trong menu ngữ cảnh.

Trong hộp thoại chỉnh sửa, có thể thay đổi mọi trường kể cả kệ thuốc. Nếu đổi kệ, mã thuốc sẽ tự động cập nhật và ảnh đính kèm được chuyển theo.

#### Xóa Thuốc

- **Cách 1**: Double-click vào dòng thuốc, sau đó nhấn nút "Xóa" trong cửa sổ chi tiết.
- **Cách 2**: Chuột phải vào dòng thuốc → chọn **"Xóa thuốc"** trong menu ngữ cảnh.

Hộp thoại xác nhận sẽ xuất hiện trước khi xoá. Thao tác không thể hoàn tác.

---

### Quản Lý Kệ Thuốc

#### Xem Danh Sách Kệ

Bảng hiển thị tất cả kệ với các cột: Mã kệ, Dãy, Cột, Sức chứa, Đã dùng, Còn lại.

Cột "Còn lại" được tô màu cam khi dưới 20% sức chứa và tô màu đỏ khi đã đầy.

#### Thêm Kệ Mới

1. Nhấn nút **"Thêm kệ"** phía trên bảng.
2. Điền thông tin kệ: Mã kệ, Khu vực (zone), Dãy, Cột, Sức chứa tối đa.
3. Nhấn **"Thêm kệ"** để xác nhận.

#### Sửa Kệ

- **Cách 1**: Double-click vào dòng kệ để mở hộp thoại chỉnh sửa.
- **Cách 2**: Chuột phải vào dòng kệ → chọn **"Chỉnh sửa kệ"**.

Có thể thay đổi thông tin vị trí và sức chứa. Lưu ý: giảm sức chứa xuống dưới số lượng đang chứa sẽ bị từ chối.

#### Xóa Kệ

Chuột phải vào dòng kệ → chọn **"Xóa kệ"**. Hộp thoại xác nhận sẽ xuất hiện.

Lưu ý: Không thể xóa kệ đang chứa thuốc.

---

### Tìm Kiếm Thuốc

1. Nhấn nút **"Tìm kiếm"** trên thanh tiêu đề hoặc nhấn `Ctrl+K`.
2. Gõ tên thuốc vào ô tìm kiếm (hỗ trợ tìm kiếm mờ — không cần chính xác hoàn toàn, ngưỡng khớp 70%).
3. Kết quả xuất hiện ngay lập tức bên dưới kèm mã thuốc, kệ, và phần trăm độ khớp.
4. Nhấn vào kết quả để chuyển sang trang Danh sách thuốc và tự động mở chi tiết thuốc đó.
5. Nhấn `Escape` hoặc nút "Đóng" để thoát hộp thoại tìm kiếm.

---

### Lọc Danh Sách Thuốc

1. Trên trang Danh sách thuốc, nhấn nút **"Lọc"**.
2. Trong hộp thoại lọc, có thể kết hợp các điều kiện:
   - Kệ thuốc
   - Khoảng giá (từ — đến)
   - Trạng thái (Hết hạn, Sắp hết hạn, Hết hàng, Tồn kho thấp, Bình thường)
3. Nhấn **"Áp dụng"** để lọc. Nhãn đếm phía trên bảng sẽ hiển thị số mục đang hiển thị trên tổng số.
4. Nhấn nút **"Xoá lọc"** (xuất hiện khi bộ lọc đang hoạt động) để trở về danh sách đầy đủ.

---

### Chuyển Đổi Giao Diện (Light / Dark Mode)

Nhấn nút chuyển theme ở góc trên phải của thanh tiêu đề hoặc nhấn `Ctrl+D` để chuyển qua lại giữa chế độ sáng và tối. Trang đang xem sẽ được giữ nguyên sau khi chuyển theme — không bị nhảy về Dashboard.

---

### Phím Tắt

| Phím Tắt | Chức Năng |
|----------|-----------|
| `Ctrl+K` | Mở hộp thoại tìm kiếm nhanh |
| `Ctrl+D` | Chuyển đổi giữa Light Mode và Dark Mode |
| `Escape` | Đóng hộp thoại tìm kiếm |

## Cấu Trúc Dự Án

```
KiThuatLapTrinhNhom3/
├── app.py                      # 🚀 Điểm vào (QApplication setup)
├── requirements.txt            # Các phụ thuộc
├── run.bat                     # Script khởi chạy Windows
├── src/                        # Mã nguồn
│   ├── __init__.py             # Xuất package (Medicine, Shelf, v.v.)
│   ├── models.py               # Model dữ liệu: Medicine, Shelf
│   ├── storage.py              # StorageEngine: đọc/ghi JSON nguyên tử
│   ├── inventory_manager.py    # InventoryManager: CRUD, validate, sắp xếp
│   ├── alerts.py               # AlertSystem: cảnh báo hết hạn & tồn kho
│   ├── search_engine.py        # SearchEngine: tìm kiếm mờ
│   ├── image_manager.py        # ImageManager: ảnh thuốc
│   ├── dashboard_manager.py    # DashboardManager: xử lý dữ liệu dashboard
│   │
│   ├── views/                  # Các trang chính
│   │   ├── dashboard.py        # Giao diện dashboard (KPI + biểu đồ)
│   │   ├── inventory_view.py   # Bảng danh sách thuốc
│   │   └── shelf_view.py       # Trang quản lý kệ
│   │
│   ├── dialogs/                # Các hộp thoại
│   │   ├── medicine_dialog.py      # Thêm/Sửa thuốc
│   │   ├── shelf_dialog.py         # Thêm/Sửa kệ
│   │   ├── filter_dialog.py        # Lọc thuốc
│   │   ├── medicine_detail_view.py # Xem chi tiết thuốc
│   │   └── notification_dialogs.py # Thông báo thành công/lỗi/xác nhận
│   │
│   └── ui/                     # Giao diện người dùng
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
│       └── generated/           # TỰ ĐỘNG SINH — KHÔNG CHỈNH SỬA
│           ├── main_window_ui.py / main_window_ui_dark.py
│           ├── search.py / search_dark.py
│           ├── them_thuoc.py / them_thuoc_dark.py
│           ├── them_ke.py / them_ke_dark.py
│           ├── loc_thuoc.py / loc_thuoc_dark.py
│           └── ... (các dialog notification sáng + tối)
│
├── data/                       # Lưu trữ dữ liệu
│   ├── medicines.json          # CSDL thuốc
│   ├── shelves.json            # CSDL kệ
│   ├── settings.json           # Cài đặt (theme, ngưỡng)
│   └── images/                 # Ảnh thuốc
└── Ui Qt/                      # File .ui gốc Qt Designer (cặp Sáng + Tối)
    ├── main_window.ui / main_window_dark.ui
    ├── them_thuoc.ui / them_thuoc_dark.ui
    ├── them_ke.ui / them_ke_dark.ui
    ├── loc_thuoc.ui / loc_thuoc_dark.ui
    ├── search.ui / search_dark.ui
    └── ... (notification dialogs sáng + tối)
```
##  Công Nghệ

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3.13+ |
| UI Framework | PyQt6 ≥ 6.6.0 |
| Charts | Matplotlib ≥ 3.8.0 |
| Fuzzy Search | TheFuzz ≥ 0.22.0 + python-Levenshtein |
| UI Design | Qt Designer (.ui files) |
| Data Storage | JSON files |

##  Kiến Trúc

| Pattern | Mô tả |
|---------|--------|
| **MVC** | Models (`models.py`) — Views (`views/`, `dialogs/`) — Controller (`inventory_manager.py`, `dashboard_manager.py`) |
| **Repository** | `StorageEngine` trừu tượng hóa file I/O |
| **Immutable Update** | `update_medicine()` tạo object mới thay vì mutate |
| **Atomic Write** | Ghi file qua temp → rename, có backup recovery |
| **Signal/Slot** | Hệ thống sự kiện Qt cho giao tiếp UI |
| **Observer** | Dashboard + InventoryView lắng nghe thay đổi data |
| **Dual UI** | Mỗi dialog có 2 generated files (sáng + tối), chọn tại runtime |


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

Nhóm 3