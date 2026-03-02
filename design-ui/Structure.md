# 🎨 Cấu trúc Thiết kế UI/UX - Hệ thống Quản lý Nhà thuốc

Tài liệu này hệ thống hóa các thành phần giao diện trên Figma, đóng vai trò là bản hướng dẫn (Blueprints) để hiện thực hóa ứng dụng bằng PyQt6.

---

## 📄 Page 1: Design Tokens (Quy chuẩn thiết kế)
Đây là "xương sống" đảm bảo tính nhất quán cho toàn bộ giao diện ứng dụng.

### 1.1. Hệ thống Typography & Spacing
* **Phông chữ (Font):** Ưu tiên nhóm Sans-serif trung tính (như **Inter** hoặc **Roboto**) để đảm bảo sự sạch sẽ và chuyên nghiệp trong môi trường y tế.
* **Tiêu đề trang (H1):** Kích thước 20–22px, định dạng **SemiBold**.
* **Văn bản nội dung (Body):** Kích thước 14px, định dạng **Regular**.
* **Hệ thống Lưới (Grid):** Sử dụng đơn vị cơ bản là **8px** cho tất cả các khoảng cách Margin, Padding và Gap để tạo sự hài hòa.

---

## 🏗️ Page 2: Layout Structure (Khung sườn ứng dụng)
Thiết kế dựa trên kích thước cửa sổ chuẩn **1440x1024** (theo cấu trúc code `app.py`) và chia làm 3 khu vực chức năng cố định:

* **Sidebar (Bên trái):** Chiếm ~20% chiều ngang, sử dụng `QListWidget` để điều hướng chính: Dashboard, Inventory, Reports, Settings.
* **Main Area (Trung tâm):** Chiếm ~80% chiều ngang, sử dụng `QStackedWidget` để thay đổi nội dung trang hiển thị dựa trên lựa chọn từ Sidebar.




---

## 🖼️ Page 3: App Screens (Chi tiết các trang)

### 3.1. Màn hình Dashboard (Tổng quan)
Tập trung hiển thị thông tin quan trọng một cách trực quan để dược sĩ nắm bắt nhanh tình trạng kho.

* **Dãy thẻ chỉ số (4 KPI Cards):**
    * **Thẻ 1:** Tổng kho (Màu trung tính).
    * **Thẻ 2:** Sắp hết hạn trong 30 ngày (Màu Vàng).
    * **Thẻ 3:** Đã hết hạn (Màu Đỏ).
    * **Thẻ 4:** Tồn kho thấp (Màu Cam/Vàng).
* **Khu vực Biểu đồ (Charts):**
    * **Biểu đồ tròn:** Phân bổ tình trạng hạn sử dụng (Còn hạn, Sắp hết hạn, Đã hết hạn).
    * **Biểu đồ cột:** Top 10 loại thuốc có số lượng tồn kho nhiều nhất.
* **Danh sách hành động (Quick Lists):** Bảng nhỏ hiển thị danh sách rút gọn của các thuốc sắp hết hạn và tồn kho thấp để xử lý ngay.



### 3.2. Màn hình Inventory (Quản lý kho)
Thiết kế tối ưu cho việc quan sát và thao tác dữ liệu bảng lớn.

* **Thanh công cụ (Toolbar):** Thanh tìm kiếm (Fuzzy search) nằm bên trái; nút "Add Medicine" (biểu tượng `+`) nằm bên phải.
* **Bảng dữ liệu (Data Table):** Sử dụng `QTableView` hiển thị 6 cột: Name, Quantity, Expiry Date, Shelf, Price, Status.
* **Định dạng có điều kiện (Conditional Styles):**
    * **Thuốc đã hết hạn:** Sử dụng nền đỏ nhạt và chữ đỏ đậm.
    * **Thuốc sắp hết hạn:** Sử dụng nền vàng nhạt và chữ vàng đậm.

### 3.3. Overlays (Hộp thoại & Modal)
Các khung hình (Frame) rời hiển thị đè lên giao diện chính.

* **Add/Edit Dialog:** Hộp thoại Modal gồm 5 trường nhập liệu: Name, Quantity (SpinBox), Expiry (DateEdit), Shelf (ComboBox), và Price.
* **Global Search (Ctrl+K):** Một thanh tìm kiếm tối giản xuất hiện giữa màn hình kèm danh sách kết quả hiển thị Tên thuốc và % khớp.

---

## 💡 Lưu ý về tương tác (Prototype)
Xây dựng luồng (Flow) trên Figma bám sát sơ đồ quy trình nghiệp vụ:

1.  **Luồng Nhập/Xuất:** Tìm kiếm thuốc -> Nếu đã tồn tại thì tăng số lượng; Nếu chưa có thì mở Modal "Add Medicine" để nhập mới.
2.  **Luồng Chỉnh sửa:** Nhấp đúp chuột vào hàng hoặc chuột phải chọn Edit -> Hiển thị Pop-up Dialog để cập nhật thông tin.
3.  **Luồng Xóa:** Yêu cầu xác nhận qua `QMessageBox` trước khi thực hiện xóa, đặc biệt khi thuốc vẫn còn tồn kho.