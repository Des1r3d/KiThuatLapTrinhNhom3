# Tài Liệu ClassFlow — Hệ Thống Quản Lý Kho Thuốc

Tài liệu này mô tả chi tiết luồng xử lý và mẫu tương tác của từng lớp (class) trong Hệ Thống Quản Lý Kho Thuốc.

## Mục Lục
1. [Lớp Medicine](#1-lớp-medicine)
2. [Lớp Shelf](#2-lớp-shelf)
3. [Luồng InventoryManager](#3-luồng-inventorymanager)
4. [Luồng StorageEngine](#4-luồng-storageengine)
5. [Luồng SearchEngine](#5-luồng-searchengine)
6. [Luồng DashboardManager](#6-luồng-dashboardmanager)
7. [Luồng Thành Phần UI](#7-luồng-thành-phần-ui)
8. [Luồng Tích Hợp](#8-luồng-tích-hợp)
9. [Luồng Xử Lý Lỗi](#9-luồng-xử-lý-lỗi)

---

## 1. Lớp Medicine

### Mục đích
Model dữ liệu chính đại diện cho một mục thuốc trong kho.

### Thuộc tính
- `id: str` - Mã định danh duy nhất (tự sinh nếu rỗng)
- `name: str` - Tên thuốc
- `quantity: int` - Số lượng tồn kho (phải >= 0)
- `expiry_date: date` - Ngày hết hạn
- `shelf_id: str` - Tham chiếu tới vị trí lưu trữ
- `price: float` - Đơn giá

### Luồng phương thức

#### `is_expired() -> bool`
```
BẮT ĐẦU
  ↓
Lấy ngày hiện tại
  ↓
So sánh expiry_date với hôm nay
  ↓
Trả về True nếu expiry_date < hôm nay
  ↓
KẾT THÚC
```

#### `days_until_expiry() -> int`
```
BẮT ĐẦU
  ↓
Lấy ngày hiện tại
  ↓
Tính delta = expiry_date - hôm nay
  ↓
Trả về delta.days (âm nếu đã hết hạn)
  ↓
KẾT THÚC
```

#### `to_dict() -> dict`
```
BẮT ĐẦU
  ↓
Tạo dictionary rỗng
  ↓
Với mỗi thuộc tính:
  - Chuyển đổi sang kiểu JSON-serializable
  - Xử lý date → chuỗi ISO
  ↓
Trả về dictionary
  ↓
KẾT THÚC
```

#### `from_dict(data: dict) -> Medicine`
```
BẮT ĐẦU
  ↓
Kiểm tra các trường bắt buộc tồn tại
  ↓
Phân tích chuỗi ngày → đối tượng date
  ↓
Tạo thực thể Medicine
  ↓
Kiểm tra ràng buộc (qty >= 0)
  ↓
Trả về đối tượng Medicine
  ↓
KẾT THÚC
```

### Chuyển đổi trạng thái
```
[Mới] → [Hợp lệ] → [Trong kho]
           ↓
      [Hết hạn] (khi expiry_date < hôm nay)
           ↓
      [Tồn kho thấp] (khi quantity < ngưỡng)
```

---

## 2. Lớp Shelf

### Mục đích
Đại diện cho vị trí lưu trữ vật lý trong nhà thuốc.

### Thuộc tính
- `id: str` - Mã kệ
- `row: str` - Vị trí hàng
- `column: str` - Vị trí cột
- `capacity: str` - Sức chứa tối đa

### Luồng phương thức

#### `to_dict() -> dict`
```
BẮT ĐẦU
  ↓
Chuyển đổi tất cả thuộc tính thành dictionary
  ↓
Trả về dictionary
  ↓
KẾT THÚC
```

#### `from_dict(data: dict) -> Shelf`
```
BẮT ĐẦU
  ↓
Kiểm tra các trường bắt buộc
  ↓
Tạo thực thể Shelf
  ↓
Trả về đối tượng Shelf
  ↓
KẾT THÚC
```

### Sử dụng trong hệ thống
```
Người dùng chọn kệ (Dropdown trong Dialog Thêm/Sửa)
  ↓
InventoryManager kiểm tra shelf_id tồn tại
  ↓
Medicine.shelf_id tham chiếu Shelf.id
  ↓
Hiển thị vị trí trong Bảng kho
```

---

## 3. Luồng InventoryManager

### Mục đích
Bộ điều khiển trung tâm cho tất cả thao tác kho. Quản lý CRUD và logic nghiệp vụ.

### Phụ thuộc
- `StorageEngine` - Để lưu trữ bền vững
- `Medicine` - Model dữ liệu
- `SearchEngine` - Cho thao tác tìm kiếm

### Luồng phương thức

#### `load_data()`
```
BẮT ĐẦU
  ↓
Gọi StorageEngine.read_json('medicines.json')
  ↓
Nhận danh sách dictionaries
  ↓
Với mỗi dict:
  - Medicine.from_dict(dict)
  - Thêm vào self.medicines
  ↓
Xử lý FileNotFoundError → Khởi tạo danh sách rỗng
  ↓
Xử lý JSONDecodeError → Ghi log, dùng bản sao lưu
  ↓
KẾT THÚC
```

#### `save_data()`
```
BẮT ĐẦU
  ↓
Với mỗi Medicine trong self.medicines:
  - Gọi medicine.to_dict()
  - Thu thập vào danh sách
  ↓
Gọi StorageEngine.write_json('medicines.json', data)
  ↓
Xử lý lỗi → Khôi phục trạng thái trước
  ↓
KẾT THÚC
```

#### `add_medicine(medicine: Medicine)`
```
BẮT ĐẦU
  ↓
Kiểm tra dữ liệu thuốc
  ↓
Kiểm tra medicine.id có rỗng không
  ↓
  CÓ → Tự sinh ID duy nhất
  ↓
Kiểm tra quantity >= 0
  ↓
Kiểm tra expiry_date >= hôm nay (cảnh báo nếu đã qua)
  ↓
Kiểm tra shelf_id tồn tại
  ↓
Thêm vào self.medicines
  ↓
Gọi save_data()
  ↓
Phát tín hiệu → UI cập nhật bảng
  ↓
KẾT THÚC
```

#### `remove_medicine(medicine_id: str)`
```
BẮT ĐẦU
  ↓
Tìm thuốc theo ID trong self.medicines
  ↓
  KHÔNG TÌM THẤY → Ném ValueError
  ↓
Xóa khỏi danh sách
  ↓
Gọi save_data()
  ↓
Phát tín hiệu → UI cập nhật bảng
  ↓
KẾT THÚC
```

#### `update_medicine(medicine_id: str, changes: dict)`
```
BẮT ĐẦU
  ↓
Tìm thuốc theo ID
  ↓
  KHÔNG TÌM THẤY → Ném ValueError
  ↓
Tạo đối tượng Medicine mới (mẫu bất biến)
  ↓
Áp dụng thay đổi vào đối tượng mới
  ↓
Kiểm tra đối tượng mới
  ↓
Thay thế đối tượng cũ trong danh sách
  ↓
Gọi save_data()
  ↓
Phát tín hiệu → UI cập nhật
  ↓
KẾT THÚC
```

#### `check_expiry(days_threshold: int = 30) -> List[Medicine]`
```
BẮT ĐẦU
  ↓
Khởi tạo danh sách kết quả rỗng
  ↓
Với mỗi thuốc trong self.medicines:
  - Tính days_until_expiry()
  - Nếu days <= days_threshold:
    → Thêm vào danh sách kết quả
  ↓
Sắp xếp theo expiry_date (sớm nhất trước)
  ↓
Trả về danh sách kết quả
  ↓
KẾT THÚC
```

#### `check_low_stock(threshold: int = 5) -> List[Medicine]`
```
BẮT ĐẦU
  ↓
Khởi tạo danh sách kết quả rỗng
  ↓
Với mỗi thuốc trong self.medicines:
  - Nếu quantity <= threshold:
    → Thêm vào danh sách kết quả
  ↓
Sắp xếp theo quantity (thấp nhất trước)
  ↓
Trả về danh sách kết quả
  ↓
KẾT THÚC
```

---

## 4. Luồng StorageEngine

### Mục đích
Xử lý thao tác file JSON nguyên tử với xử lý lỗi.

### Luồng phương thức

#### `read_json(filepath: str) -> dict`
```
BẮT ĐẦU
  ↓
Kiểm tra file tồn tại
  ↓
  KHÔNG → Ném FileNotFoundError
  ↓
Mở file ở chế độ đọc
  ↓
Thử: json.load(file)
  ↓
  JSONDecodeError → Kiểm tra file sao lưu
    ↓
    Có bản sao lưu? → Tải bản sao lưu
    ↓
    Không có? → Ném lỗi
  ↓
Trả về dữ liệu đã phân tích
  ↓
KẾT THÚC
```

#### `write_json(filepath: str, data: dict)`
```
BẮT ĐẦU
  ↓
Tạo bản sao lưu file hiện tại (nếu có)
  ↓
Tạo tên file tạm: filepath + '.tmp'
  ↓
Mở file tạm ở chế độ ghi
  ↓
json.dump(data, file, indent=2)
  ↓
Đóng file tạm
  ↓
Đổi tên nguyên tử: temp → filepath
  ↓
  THÀNH CÔNG → Xóa bản sao lưu
  ↓
  THẤT BẠI → Khôi phục từ bản sao lưu, ném lỗi
  ↓
KẾT THÚC
```

### Xử lý lỗi
```
Thao tác ghi:
  ↓
Sao lưu → Ghi vào .tmp → Đổi tên
  ↓               ↓               ↓
  LỖI           LỖI            LỖI
  ↓               ↓               ↓
Ghi log    Khôi phục sao lưu  Khôi phục sao lưu
  ↓               ↓               ↓
Ném lỗi   Ném lỗi           Ném lỗi
```

---

## 5. Luồng SearchEngine

### Mục đích
Triển khai tìm kiếm mờ sử dụng thư viện TheFuzz.

### Phụ thuộc
- Thư viện `thefuzz` (khớp mờ)
- Danh sách `Medicine` từ InventoryManager

### Luồng phương thức

#### `index_data(medicines: List[Medicine])`
```
BẮT ĐẦU
  ↓
Xóa chỉ mục hiện tại
  ↓
Với mỗi thuốc:
  - Trích xuất tên
  - Lưu vào dict chỉ mục: {id: name}
  ↓
Cache chỉ mục để tra cứu nhanh
  ↓
KẾT THÚC
```

#### `search(query: str, limit: int = 5) -> List[Tuple[Medicine, int]]`
```
BẮT ĐẦU
  ↓
Chuẩn hóa truy vấn (viết thường, cắt khoảng trắng)
  ↓
Khởi tạo danh sách kết quả
  ↓
Với mỗi thuốc trong chỉ mục:
  - Tính điểm khớp mờ cho tên (fuzz.ratio)
  - Sử dụng name_score
  ↓
Lọc kết quả: score >= 80
  ↓
Sắp xếp theo điểm (giảm dần)
  ↓
Lấy 'limit' kết quả đầu
  ↓
Trả về List[(đối tượng Medicine, score)]
  ↓
KẾT THÚC
```

### Thuật toán khớp mờ
```
Đầu vào: query = "paracetamol"
  ↓
Với medicine.name = "Paracetamol 500mg":
  - fuzz.ratio("paracetamol", "paracetamol 500mg") → 85
  ↓
Với medicine.name = "Aspirin":
  - fuzz.ratio("paracetamol", "aspirin") → 30
  ↓
Lọc: Chỉ giữ score >= 80
  ↓
Kết quả: [("Paracetamol 500mg", 85)]
```

---

---

## 6. Luồng DashboardManager

> **Vị trí:** `src/dashboard_manager.py`

### Mục đích
Xử lý toàn bộ logic nghiệp vụ cho trang Dashboard. Tách biệt hoàn toàn khỏi tầng view.

### 6.1 Luồng MainWindow

> **Vị trí:** `src/ui/main_window.py`

#### Khởi tạo
```
BẮT ĐẦU
  ↓
Tạo QMainWindow
  ↓
Thiết lập điều hướng sidebar (QListWidget)
  ↓
Tạo QStackedWidget cho vùng chính
  ↓
Thêm trang: Dashboard, InventoryView, ShelfView
  ↓
Thiết lập phím tắt:
  - Ctrl+K → Mở modal tìm kiếm
  ↓
Kết nối tín hiệu:
  - Mục sidebar được nhấn → Chuyển trang
  - Các hành động menu → Mở hộp thoại
  ↓
Tải cài đặt người dùng (chủ đề, kích thước cửa sổ)
  ↓
Hiện cửa sổ
  ↓
KẾT THÚC
```

### 6.2 Luồng Dashboard

> **Vị trí:** `src/views/dashboard.py`
> **Generated UI:** `src/ui/generated/dashboard_ui.py` (từ `Ui Qt/dashboard.ui`)

#### Mục đích
Hiển thị số liệu thống kê tổng quan và biểu đồ bằng Matplotlib.
Sử dụng `Ui_DashboardWidget` (generated) cho layout — chỉ chứa mã render, logic nằm ở `DashboardManager`.

#### Kiến trúc UI
- **4 KPI Card Frames**: `card_total`, `card_expiring`, `card_expired`, `card_low_stock`
  - Mỗi card: `lbl_*_title`, `lbl_*_value`, `lbl_*_subtitle` (defined in .ui)
  - Styling: `Theme.get_stat_card_style()` áp dụng runtime
- **2 Chart Placeholders**: `widget_pie_placeholder`, `widget_bar_placeholder` (QWidget)
  - Được thay thế bằng `FigureCanvasQTAgg` tại runtime
- **2 Alert Tables**: `tbl_expiry` (3 cột), `tbl_stock` (3 cột)

#### Luồng khởi tạo
```
BẮT ĐẦU
  ↓
Tạo Ui_DashboardWidget() → setupUi(self)
  ↓
Thay thế widget_pie_placeholder bằng FigureCanvasQTAgg
  ↓
Thay thế widget_bar_placeholder bằng FigureCanvasQTAgg
  ↓
Cấu hình table headers (Stretch + ResizeToContents)
  ↓
Áp dụng card stylesheet: Theme.get_stat_card_style(card_type)
  ↓
Đặt objectName cho chart/alert frames (cho theme CSS)
  ↓
Gọi _apply_theme()
  ↓
KẾT THÚC
```

#### Luồng tải dữ liệu (load_data)
```
Nhận danh sách medicines từ MainWindow
  ↓
Ủy quyền cho DashboardManager:
  - get_statistics() → DashboardStats
  - get_pie_chart_data() → PieChartData
  - get_bar_chart_data() → BarChartData
  - get_expiring_medicines() → List[ExpiryItem]
  - get_low_stock_medicines() → List[LowStockItem]
  ↓
Render KPI cards (_render_statistics)
  ↓
Render biểu đồ tròn (_render_pie_chart)
  ↓
Render biểu đồ cột (_render_bar_chart)
  ↓
Render bảng cảnh báo hết hạn (_render_expiry_table)
  ↓
Render bảng tồn kho thấp (_render_stock_table)
  ↓
KẾT THÚC
```

### 6.3 Luồng InventoryView

> **Vị trí:** `src/views/inventory_view.py`
> **Generated UI:** `src/ui/generated/inventory_view_ui.py` (từ `Ui Qt/inventory_view.ui`)

#### Mục đích
Hiển thị thuốc trong bảng có thể sắp xếp/lọc. Sử dụng `Ui_InventoryView` (generated) cho layout.

#### Widgets (defined trong .ui)
- `lbl_title`, `btn_add`, `btn_filter`, `btn_clear_filter`, `lbl_count`
- `tbl_medicines`: QTableWidget 7 cột (ID, TÊN THUỐC, SỐ LƯỢNG, HSD, KỆ, GIÁ, TRẠNG THÁI)

#### Luồng khởi tạo
```
BẮT ĐẦU
  ↓
Tạo Ui_InventoryView() → setupUi(self)
  ↓
Cấu hình column resize modes (Stretch cho cột Tên)
  ↓
Đặt row height = 42px
  ↓
Kết nối tín hiệu:
  - btn_add.clicked → add_requested signal
  - btn_filter.clicked → filter_requested signal
  - btn_clear_filter.clicked → clear_filters()
  - tbl_medicines.itemDoubleClicked → detail_requested signal
  - tbl_medicines.customContextMenuRequested → show_context_menu()
  ↓
KẾT THÚC
```

#### Luồng cập nhật dữ liệu
```
MainWindow gọi load_medicines(medicines)
  ↓
Áp dụng bộ lọc hiện tại (nếu có)
  ↓
Xóa bảng, thêm từng hàng:
  - Status badge (pill shape) với mã màu từ Theme.get_alert_colors()
  - Hàng nào có trạng thái danger/warning → text color toàn hàng
  ↓
Cập nhật lbl_count (hiện tổng/lọc)
  ↓
KẾT THÚC
```

### 6.4 Luồng Hộp Thoại Thêm/Sửa

> **Vị trí:** `src/dialogs/medicine_dialog.py`
> **Generated UI:** `src/ui/generated/them_thuoc.py` (từ `Ui Qt/them_thuoc.ui`)

#### Mục đích
Form để tạo/chỉnh sửa mục thuốc. Sử dụng `Ui_dlg_medicine_detail` (generated) cho layout.

#### Luồng khởi tạo
```
BẮT ĐẦU
  ↓
Tạo QDialog
  ↓
Chọn UI class theo theme (light/dark)
  ↓
SetupUi → Các trường form:
  - QLineEdit: Tên, Hoạt chất, Giá
  - QSpinBox: Số lượng
  - QDateEdit: Hạn sử dụng
  - QComboBox: Kệ (lấy từ shelves.json)
  ↓
Nếu chế độ SỬA:
  - Điền sẵn dữ liệu thuốc hiện tại
  ↓
Kết nối nút:
  - Lưu → validate_and_save()
  - Hủy → close()
  ↓
KẾT THÚC
```

#### Luồng lưu
```
Người dùng nhấn nút Lưu
  ↓
Kiểm tra tất cả trường
  ↓
  KHÔNG HỢP LỆ → Hiện thông báo lỗi, quay lại
  ↓
Tạo đối tượng Medicine từ dữ liệu form
  ↓
Nếu chế độ THÊM:
  - Gọi InventoryManager.add_medicine()
  ↓
Nếu chế độ SỬA:
  - Gọi InventoryManager.update_medicine()
  ↓
InventoryManager lưu vào JSON
  ↓
InventoryManager phát tín hiệu
  ↓
Hộp thoại đóng
  ↓
InventoryView tự động cập nhật
  ↓
KẾT THÚC
```

### 6.5 Luồng Modal Tìm Kiếm Toàn Cục

> **Vị trí:** `src/ui/main_window.py` (SearchDialog nội tuyến)
> **Generated UI:** `src/ui/generated/search.py` (từ `Ui Qt/search.ui`)

#### Mục đích
Tìm kiếm nhanh qua phím tắt Ctrl+K.

#### Luồng kích hoạt
```
Người dùng nhấn Ctrl+K
  ↓
Tạo/Hiện modal tìm kiếm (QDialog)
  ↓
Focus vào QLineEdit
  ↓
Người dùng gõ truy vấn
  ↓
Khi text thay đổi:
  - Gọi SearchEngine.search(query)
  - Hiển thị kết quả trong QListWidget
  - Hiện điểm cho mỗi kết quả
  ↓
Người dùng chọn kết quả
  ↓
Chuyển đến InventoryView
  ↓
Đánh dấu thuốc đã chọn trong bảng
  ↓
Đóng modal
  ↓
KẾT THÚC
```

### 6.6 Luồng ShelfView

> **Vị trí:** `src/views/shelf_view.py`
> **Generated UI:** `src/ui/generated/shelf_view_ui.py` (từ `Ui Qt/shelf_view.ui`)

#### Mục đích
Hiển thị và quản lý kệ thuốc. Sử dụng `Ui_ShelfView` (generated) cho layout.

#### Widgets (defined trong .ui)
- `lbl_title`, `btn_add`, `lbl_count`
- `tbl_shelves`: QTableWidget 6 cột (ID Kệ, Dãy, Cột, Sức chứa, Đã dùng, Còn lại)

#### Luồng khởi tạo
```
BẮT ĐẦU
  ↓
Tạo Ui_ShelfView() → setupUi(self)
  ↓
Cấu hình column resize modes
  ↓
Kết nối tín hiệu:
  - btn_add.clicked → add_requested signal
  - tbl_shelves.itemDoubleClicked → edit_requested signal
  - tbl_shelves.customContextMenuRequested → show_context_menu()
  ↓
KẾT THÚC
```

#### Luồng tải dữ liệu
```
MainWindow gọi load_shelves(shelves, medicines_per_shelf)
  ↓
Xóa bảng, thêm từng hàng:
  - Cột "Còn lại" = capacity - used
  - Mã màu: đỏ nếu ≤ 0, cam nếu ≤ 20% capacity
  ↓
Cập nhật lbl_count
  ↓
KẾT THÚC
```

---

## 8. Luồng Tích Hợp

### 8.1 Luồng Thêm Thuốc Hoàn Chỉnh (Tất Cả Tầng)

```
[Tầng UI]
Người dùng nhấn nút "Thêm thuốc"
  ↓
MainWindow mở MedicineDialog
  ↓
Người dùng điền form và nhấn Lưu
  ↓
Dialog kiểm tra đầu vào
  ↓

[Tầng Logic Nghiệp Vụ]
Dialog tạo đối tượng Medicine
  ↓
Gọi InventoryManager.add_medicine(medicine)
  ↓
InventoryManager kiểm tra:
  - Tự sinh ID nếu rỗng
  - Kiểm tra quantity >= 0
  - Kiểm tra shelf_id tồn tại
  ↓
InventoryManager thêm vào danh sách thuốc
  ↓

[Tầng Dữ Liệu]
InventoryManager gọi save_data()
  ↓
Chuyển đổi thuốc thành danh sách dict
  ↓
Gọi StorageEngine.write_json()
  ↓
StorageEngine thực hiện ghi nguyên tử:
  - Tạo bản sao lưu
  - Ghi vào file .tmp
  - Đổi tên .tmp → medicines.json
  ↓

[Quay lại Tầng UI]
InventoryManager phát tín hiệu 'medicine_added'
  ↓
InventoryView nhận tín hiệu
  ↓
InventoryView tải lại dữ liệu
  ↓
Bảng cập nhật với thuốc mới
  ↓
Thanh trạng thái hiện số lượng mới
  ↓
Hộp thoại đóng
  ↓
KẾT THÚC
```

### 8.2 Luồng Tìm Kiếm (Tất Cả Tầng)

```
[Tầng UI]
Người dùng nhấn Ctrl+K
  ↓
SearchModal mở
  ↓
Người dùng gõ "paracet"
  ↓
Sự kiện text changed của SearchModal
  ↓

[Tầng Logic Nghiệp Vụ]
Gọi SearchEngine.search("paracet")
  ↓
SearchEngine thực hiện khớp mờ:
  - So sánh với tất cả tên thuốc
  - Tính điểm
  - Lọc score >= 80
  - Sắp xếp theo điểm
  ↓
Trả về List[(Medicine, score)]
  ↓

[Quay lại Tầng UI]
SearchModal hiển thị kết quả:
  - "Paracetamol 500mg (95%)"
  - "Paracetamol Extra (88%)"
  ↓
Người dùng chọn kết quả đầu
  ↓
SearchModal phát tín hiệu 'medicine_selected'
  ↓
MainWindow chuyển sang InventoryView
  ↓
InventoryView đánh dấu thuốc đã chọn
  ↓
SearchModal đóng
  ↓
KẾT THÚC
```

### 8.3 Luồng Làm Mới Dashboard

```
[Tầng UI]
Widget Dashboard được hiển thị
  ↓
Dashboard gọi load_data(medicines)
  ↓

[Tầng Logic Nghiệp Vụ - DashboardManager]
Gọi get_statistics(medicines) → DashboardStats
  ↓
Gọi get_pie_chart_data(medicines) → PieChartData
  ↓
Gọi get_bar_chart_data(medicines) → BarChartData
  ↓
Gọi get_expiring_medicines(medicines) → List[ExpiryItem]
  ↓
Gọi get_low_stock_medicines(medicines) → List[LowStockItem]
  ↓

[Quay lại Tầng UI - Dashboard View]
Render thẻ KPI với DashboardStats
  ↓
Render biểu đồ tròn với PieChartData
  ↓
Render biểu đồ cột với BarChartData
  ↓
Điền bảng sắp hết hạn với List[ExpiryItem]
  ↓
Điền bảng tồn kho thấp với List[LowStockItem]
  ↓
KẾT THÚC
```

---

## 9. Luồng Xử Lý Lỗi

### 9.1 Lỗi Tầng Dữ Liệu

#### Không tìm thấy file
```
StorageEngine.read_json('medicines.json')
  ↓
Ném FileNotFoundError
  ↓
Kiểm tra file sao lưu
  ↓
  Có sao lưu? → Tải bản sao lưu, cảnh báo người dùng
  ↓
  Không có? → Trả về danh sách rỗng, ghi log cảnh báo
  ↓
InventoryManager khởi tạo với danh sách thuốc rỗng
  ↓
UI hiển thị "Không tìm thấy thuốc"
```

#### Lỗi giải mã JSON
```
StorageEngine.read_json('medicines.json')
  ↓
Ném JSONDecodeError (file bị hỏng)
  ↓
Kiểm tra file sao lưu
  ↓
  Có sao lưu? → Tải bản sao lưu, cảnh báo người dùng
  ↓
  Không có? → Hiện hộp thoại lỗi, thoát an toàn
  ↓
Ghi log lỗi với stack trace
```

#### Lỗi ghi file
```
StorageEngine.write_json()
  ↓
IOError khi ghi (đĩa đầy, từ chối quyền)
  ↓
Khôi phục: Phục hồi từ bản sao lưu
  ↓
Hiện hộp thoại lỗi cho người dùng
  ↓
Ghi log chi tiết lỗi
  ↓
Giữ trạng thái bộ nhớ hiện tại (không mất thay đổi)
```

### 9.2 Lỗi Logic Nghiệp Vụ

#### Dữ liệu thuốc không hợp lệ
```
InventoryManager.add_medicine(medicine)
  ↓
Kiểm tra thất bại (quantity < 0)
  ↓
Ném ValueError với thông báo
  ↓
Dialog bắt ngoại lệ
  ↓
Hiện thông báo lỗi: "Số lượng phải >= 0"
  ↓
Focus vào trường không hợp lệ
  ↓
Người dùng chỉnh sửa và thử lại
```

#### ID trùng lặp
```
InventoryManager.add_medicine(medicine)
  ↓
Kiểm tra medicine.id đã tồn tại
  ↓
  TỒN TẠI → Ném ValueError("ID trùng lặp")
  ↓
Dialog hiện lỗi
  ↓
Tự sinh ID mới
  ↓
Thử lại
```

### 9.3 Lỗi Tầng UI

#### Đầu vào form không hợp lệ
```
Người dùng nhập ngày không hợp lệ
  ↓
Kiểm tra QDateEdit thất bại
  ↓
Hiện thông báo lỗi nội tuyến
  ↓
Vô hiệu hóa nút Lưu cho đến khi sửa
```

#### Tìm kiếm không có kết quả
```
SearchEngine.search(query)
  ↓
Trả về danh sách rỗng (không khớp >= 80%)
  ↓
SearchModal hiển thị: "Không tìm thấy kết quả"
  ↓
Gợi ý người dùng thử từ khóa khác
```

---

## 10. Sơ Đồ Máy Trạng Thái

### 10.1 Trạng thái ứng dụng
```
[Khởi động]
  ↓
[Đang tải dữ liệu] → LỖI → [Trạng thái lỗi] → [Phục hồi]
  ↓                                                  ↓
[Sẵn sàng]                                    [Đang tải dữ liệu]
  ↓
[Chờ] ←→ [Đang tìm kiếm] ←→ [Hiển thị kết quả]
  ↓
[Đang chỉnh sửa] → [Đang lưu] → LỖI → [Hộp thoại lỗi] → [Đang chỉnh sửa]
  ↓           ↓
[Chờ]     THÀNH CÔNG
              ↓
           [Chờ]
```

### 10.2 Trạng thái đối tượng Medicine
```
[Mới] → [Đã kiểm tra] → [Đã lưu]
                           ↓
                       [Trong kho]
                           ↓
                     [Trạng thái bình thường]
                           ↓
               ┌───────────┴───────────┐
               ↓                       ↓
         [Sắp hết hạn]          [Tồn kho thấp]
               ↓                       ↓
           [Hết hạn]              [Hết hàng]
               ↓                       ↓
           [Đã xóa]              [Đã xóa]
```

---

## 11. Cấu Trúc File và Ánh Xạ Lớp

### Tổ chức file hiện tại
```
src/
├── models.py
│   ├── Medicine
│   └── Shelf
│
├── storage.py
│   └── StorageEngine
│
├── inventory_manager.py
│   └── InventoryManager
│
├── search_engine.py
│   └── SearchEngine
│
├── alerts.py
│   └── AlertSystem
│
├── image_manager.py
│   └── ImageManager
│
├── dashboard_manager.py              # Xử lý dữ liệu dashboard
│   ├── DashboardManager
│   ├── DashboardStats (dataclass)
│   ├── PieChartData (dataclass)
│   ├── BarChartData (dataclass)
│   ├── ExpiryItem (dataclass)
│   └── LowStockItem (dataclass)
│
├── views/                            # ⚠️ Nằm trong src/, import: from src.views.xxx
│   ├── dashboard.py                  # Dashboard (dùng Ui_DashboardWidget generated)
│   ├── inventory_view.py             # Bảng thuốc (dùng Ui_InventoryView generated)
│   └── shelf_view.py                 # Quản lý kệ (dùng Ui_ShelfView generated)
│
├── dialogs/                          # ⚠️ Nằm trong src/, import: from src.dialogs.xxx
│   ├── medicine_dialog.py            # Thêm/Sửa thuốc (dùng Ui_dlg_medicine_detail)
│   ├── shelf_dialog.py               # Thêm/Sửa kệ (dùng Ui_dlg_shelf)
│   ├── filter_dialog.py              # Lọc thuốc (dùng Ui_dlg_filter)
│   ├── medicine_detail_view.py       # Xem chi tiết thuốc
│   └── notification_dialogs.py       # Thông báo thành công/lỗi
│
└── ui/
    ├── __init__.py               # Lazy imports (__getattr__) — tránh circular import
    ├── main_window.py
    │   ├── MainWindow
    │   └── SearchDialog
    │
    ├── theme/                    # Hệ thống chủ đề (đã tách module)
    │   ├── __init__.py           # Xuất Theme, ThemeMode
    │   ├── colors.py             # Bảng màu LIGHT_COLORS, DARK_COLORS
    │   ├── tokens.py             # Khoảng cách, bo góc, font chữ
    │   ├── sidebar.py            # Hằng số sidebar
    │   ├── cards.py              # Màu thẻ thống kê & biểu đồ
    │   ├── core.py               # Lớp Theme, enum ThemeMode
    │   ├── stylesheets.py        # Hàm tạo stylesheet Qt
    │   └── badges.py             # Hàm huy hiệu/cảnh báo
    │
    └── generated/                # ⚠️ TỰ ĐỘNG SINH — KHÔNG CHỈNH SỬA
        ├── main_window_ui.py / main_window_ui_dark.py
        ├── dashboard_ui.py               # ← MỚI (từ dashboard.ui)
        ├── inventory_view_ui.py          # ← MỚI (từ inventory_view.ui)
        ├── shelf_view_ui.py              # ← MỚI (từ shelf_view.ui)
        ├── them_thuoc.py / them_thuoc_dark.py
        ├── them_ke.py / them_ke_dark.py
        ├── loc_thuoc.py / loc_thuoc_dark.py
        ├── search.py / search_dark.py
        ├── them_thanh_cong.py / them_thanh_cong_dark.py
        ├── sua_thanh_cong.py / sua_thanh_cong_dark.py
        ├── xac_nhan_xoa.py / xac_nhan_xoa_dark.py
        ├── xoa_thanh_cong.py / xoa_thanh_cong_dark.py
        ├── thong_tin_thuoc.py / thong_tin_thuoc_dark.py
        └── ke_day.py
```

---

## 12. Tham Chiếu Chéo Với Tickets

| Ticket | Thành phần | Phần ClassFlow |
|--------|-----------|----------------|
| T-101 | Thiết lập dự án | N/A (Hạ tầng) |
| T-102 | Model dữ liệu | 1. Lớp Medicine, 2. Lớp Shelf |
| T-103 | Storage Engine | 4. Luồng StorageEngine |
| T-201 | Quản lý kho | 3. Luồng InventoryManager |
| T-202 | Hệ thống cảnh báo | 3. InventoryManager (check_expiry, check_low_stock) |
| T-203 | Search Engine | 5. Luồng SearchEngine |
| T-204 | Dashboard Manager | 6. Luồng DashboardManager |
| T-301 | Cửa sổ chính | 7.1 Luồng MainWindow |
| T-302 | Bảng kho | 7.3 Luồng InventoryView |
| T-303 | Hộp thoại Thêm/Sửa | 7.4 Luồng Hộp Thoại Thêm/Sửa |
| T-304 | Dashboard View | 7.2 Luồng Dashboard (CHỈ UI) |
| T-305 | Chuyển đổi chủ đề | 7.1 MainWindow (phím tắt) |

---

## Tóm Tắt

Tài liệu ClassFlow này cung cấp:
1. ✅ Luồng chi tiết cho từng lớp
2. ✅ Đặc tả đầu vào/đầu ra
3. ✅ Phụ thuộc và tương tác
4. ✅ Trình tự thực thi phương thức
5. ✅ Chuyển đổi trạng thái
6. ✅ Chiến lược xử lý lỗi
7. ✅ Luồng tích hợp xuyên suốt ba tầng
8. ✅ Ánh xạ với cấu trúc file thực tế và tickets

Tài liệu này nên được sử dụng làm bản thiết kế trong các giai đoạn triển khai để đảm bảo tất cả thành phần tuân theo mẫu luồng đã thiết kế.
