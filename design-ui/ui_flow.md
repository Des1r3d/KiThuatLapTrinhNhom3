

---

# Đặc tả Giao diện UI/UX: Hệ thống Quản lý Kho Thuốc (Beta)

Tài liệu này hệ thống lại các thành phần giao diện và luồng tương tác cho phiên bản Beta, đảm bảo tính nhất quán và tối ưu trải nghiệm cho Dược sĩ.

## 1. Thành phần chung (Global Components)

Các yếu tố này luôn xuất hiện cố định để đảm bảo tính nhất quán của hệ thống.

* **Sidebar (Thanh điều hướng):**
* **Dashboard:** Cung cấp cái nhìn tổng quan về tình trạng kho.
* **Inventory:** Quản lý chi tiết danh mục thuốc và kệ.
* **Reports & Settings:** Hiện tại ở trạng thái vô hiệu hóa (Disabled) - Dự kiến ra mắt sau phiên bản Beta.


* **Top Bar (Thanh công cụ trên cùng):**
* **Thanh tìm kiếm nhanh:** Kích hoạt bằng phím tắt `Ctrl+K`, hỗ trợ tìm kiếm mờ (fuzzy search) thông minh.
* **Chuyển đổi Giao diện:** Nút chuyển đổi nhanh giữa chế độ Sáng (Light Mode) và Tối (Dark Mode).



---

## 2. Trang Dashboard (Bảng điều hành)

Tập trung cung cấp các số liệu phân tích trực quan giúp Dược sĩ ra quyết định nhập/xuất hàng nhanh chóng.

### 2.1. Hệ thống Thẻ tóm tắt (Summary Cards)

* **Tổng kho:** Tổng số lượng đơn vị thuốc hiện có trong hệ thống.
* **Hết hạn:** Cảnh báo các thuốc đã quá hạn sử dụng - Mã màu Đỏ (`#C0392B`).
* **Sắp hết hạn:** Cảnh báo thuốc hết hạn trong vòng 30 ngày - Mã màu Vàng (`#D68910`).
* **Tồn kho thấp:** Cảnh báo thuốc có số lượng dưới ngưỡng 5 đơn vị - Mã màu Cam (`#B9770E`).

### 2.2. Hệ thống Biểu đồ (Visual Analytics)

* **Pie Chart (Tỉ lệ trạng thái):** Phân bổ phần trăm giữa thuốc Bình thường, Sắp hết hạn và Đã hết hạn.
* **Bar Chart (Top 10 tồn kho):** Hiển thị 10 loại thuốc có số lượng tồn kho cao nhất để quản lý vòng quay hàng tồn.

### 2.3. Trung tâm Cảnh báo (Alert Center)

* **Danh sách cảnh báo:** Hiển thị các dòng thông báo mới nhất theo thời gian thực (ví dụ: *"Thuốc Paracetamol đã hết hạn"*).
* **Tương tác:** Khi click vào một thông báo, hệ thống tự động mở Pop-up thông tin chi tiết của loại thuốc đó.

---

## 3. Trang Inventory (Quản lý kho)

Nơi thực hiện các thao tác nghiệp vụ cốt lõi.

### 3.1. Bảng danh sách thuốc (Main Table)

* **Thiết kế:** Dạng dòng (Row-based), hỗ trợ sắp xếp và lọc dữ liệu linh hoạt theo từng cột.
* **Các cột hiển thị:**
1. Ảnh Thumbnail (Bo góc 8px).
2. Tên thuốc.
3. Số lượng.
4. Ngày hết hạn.
5. Kệ thuốc.
6. Trạng thái (Hiển thị dạng Badge màu tương ứng với mức độ nghiêm trọng).


* **Tương tác chuột:**
* **Click trái:** Mở Pop-up xem chi tiết thông tin và ảnh bao bì lớn.
* **Click phải (Context Menu):** Menu nhanh để thực hiện "✏️ Sửa thuốc" hoặc "🗑️ Xóa thuốc".



### 3.2. Cửa sổ Thêm/Sửa thuốc (Medicine Dialog)

* **Hình ảnh:** Hỗ trợ upload file ảnh bao bì qua vùng kéo thả hoặc nút chọn file.
* **Quản lý Kệ:**
* Sử dụng danh sách thả xuống (Dropdown list) để chọn kệ có sẵn.
* **Tính năng thêm nhanh:** Tùy chọn "➕ Thêm kệ mới" ở cuối danh sách nếu kệ cần dùng chưa tồn tại.


* **Xác thực dữ liệu:** Thông báo lỗi trực quan (viền đỏ, văn bản cảnh báo) ngay tại ô nhập liệu khi có sai sót (ví dụ: giá trị âm).

### 3.3. Khu vực Cảnh báo nhanh (Mini Alert List)

Nằm ở phía cuối trang Inventory, hiển thị các mục thuốc cần chú ý khẩn cấp (hết hạn, tồn kho cực thấp) để dược sĩ dễ dàng theo dõi trong quá trình kiểm kê.



