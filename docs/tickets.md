# Danh sách Tickets Phát triển

## Giai đoạn 1: Nền tảng & Logic Cốt lõi (Foundation & Core Logic)

### T-101: Thiết lập Project & Khởi tạo Repository
-   **Mô tả:** Khởi tạo cấu trúc dự án Python.
-   **Công việc:**
    -   Tạo môi trường ảo (virtual environment).
    -   Cài đặt thư viện: `PyQt6`, `pandas`, `thefuzz`, `matplotlib`.
    -   Tạo cấu trúc thư mục: `src/`, `data/`, `tests/`, `assets/`.
    -   Tạo file `README.md` và `.gitignore`.

### T-102: Triển khai Data Models (Dataclasses)
-   **Mô tả:** Định nghĩa các cấu trúc dữ liệu chính sử dụng Python `dataclasses`.
-   **Files:** `src/models.py`
-   **Yêu cầu:**
    -   Class `Medicine`: `id`, `name`, `qty` (số lượng), `expiry` (hạn dùng), `shelf_id` (vị trí).
    -   Class `Shelf`: quản lý kệ.
    -   Bao gồm các hàm hỗ trợ: `to_dict()`, `from_dict()`.

### T-103: Storage Engine (Xử lý JSON)
-   **Mô tả:** Tạo bộ xử lý đọc/ghi JSON dùng chung.
-   **Files:** `src/storage.py`
-   **Yêu cầu:**
    -   Atomic writes (ghi vào file tạm rồi đổi tên) để tránh lỗi file.
    -   Xử lý lỗi khi file thiếu hoặc hỏng.
    -   Viết Unit tests cho các thao tác load/save.

## Giai đoạn 2: Logic Nghiệp vụ (Business Logic)

### T-201: Inventory Manager
-   **Mô tả:** Controller quản lý các hoạt động nhập xuất kho.
-   **Files:** `src/inventory_manager.py`
-   **Yêu cầu:**
    -   Các hàm: `add_item()`, `remove_item()`, `update_item()`.
    -   Validate dữ liệu (ví dụ: không cho phép số lượng âm).
    -   Tự động sinh ID nếu chưa có.

### T-202: Hệ thống cảnh báo Hết hạn & Tồn kho
-   **Mô tả:** Logic lọc các thuốc cần chú ý.
-   **Yêu cầu:**
    -   `get_expiring_soon(days=30)`: Trả về danh sách thuốc sắp hết hạn.
    -   `get_low_stock(threshold=5)`: Trả về danh sách thuốc sắp hết.

### T-203: Fuzzy Search Engine
-   **Mô tả:** Chức năng tìm kiếm mờ sử dụng `thefuzz` hoặc `rapidfuzz`.
-   **Yêu cầu:**
    -   Cache/Index tên thuốc để tìm kiếm nhanh.
    -   Trả về top 5 kết quả phù hợp nhất kèm điểm số (score).

## Giai đoạn 3: Triển khai Giao diện (UI Implementation - PyQt6)

### T-301: Main Window Layout & Navigation
-   **Mô tả:** Tạo khung sườn cho ứng dụng.
-   **Yêu cầu:**
    -   Sidebar với các nút điều hướng.
    -   `QStackedWidget` để chuyển đổi giữa các màn hình (Dashboard, Inventory, Settings).
    -   Bắt sự kiện phím tắt toàn cục `Ctrl+K`.

### T-302: Inventory Table View (Bảng kho thuốc)
-   **Mô tả:** Hiển thị danh sách thuốc trong bảng có thể sắp xếp/lọc.
-   **Yêu cầu:**
    -   Sử dụng `QTableView` với `QAbstractTableModel` tùy chỉnh (dùng Pandas/Polars làm backend).
    -   Các cột: Tên, Số lượng, Hạn dùng, Kệ, Trạng thái (Phân màu).

### T-303: Dialog Thêm/Sửa thuốc
-   **Mô tả:** Form nhập liệu thông tin thuốc.
-   **Yêu cầu:**
    -   Date picker chọn hạn sử dụng.
    -   Dropdown chọn vị trí kệ (Shelf).
    -   Validate dữ liệu trước khi submit.

### T-304: Dashboard & Tích hợp Matplotlib
-   **Mô tả:** Màn hình chính với các biểu đồ thống kê.
-   **Yêu cầu:**
    -   Nhúng `FigureCanvasQTAgg`.
    -   Vẽ: Biểu đồ trọng (Pie chart) tỉ lệ hạn sử dụng.
    -   Vẽ: Biểu đồ cột (Bar chart) mức tồn kho.

### T-305: Dark/Light Mode Toggle
-   **Mô tả:** Chức năng đổi giao diện Sáng/Tối.
-   **Yêu cầu:**
    -   Sử dụng loader cho stylesheet (QSS).
    -   Nút chuyển đổi hoặc phím tắt `Ctrl+D`.
    -   Lưu cài đặt vào `settings.json`.
