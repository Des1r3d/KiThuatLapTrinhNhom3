### **Tới: Đội ngũ Thiết kế UI/UX**
### **Từ: Đội ngũ Phát triển**
### **Chủ đề: Tóm tắt Thiết kế (Design Brief) cho Hệ thống Quản lý Nhà thuốc**

Tài liệu này cung cấp phân tích chi tiết về các thành phần giao diện người dùng và luồng trải nghiệm người dùng được yêu cầu cho Hệ thống Quản lý Nhà thuốc mới. Ứng dụng phải hiện đại, tinh gọn và trực quan cho dược sĩ.

### **1. Nguyên tắc Thiết kế Cốt lõi & Khung Ứng dụng**

-   **Công nghệ:** Giao diện người dùng (front-end) sẽ được xây dựng hoàn toàn bằng **PyQt6**.
-   **Thẩm mỹ:** Ưu tiên một thiết kế phẳng (flat design) hiện đại. Vui lòng cung cấp hướng dẫn về phong cách (QSS/CSS) cho cả **Light Theme** (Giao diện Sáng) và **Dark Theme** (Giao diện Tối).
-   **Bố cục Cửa sổ Chính:** Ứng dụng sẽ có bố cục ba phần tiêu chuẩn:
    1.  **Sidebar (Bên trái):** Một `QListWidget` hoặc widget tương tự để điều hướng chính.
    2.  **Main Area (Khu vực chính - Trung tâm):** Một `QStackedWidget` để hiển thị chế độ xem (view) đang hoạt động dựa trên lựa chọn từ sidebar.
    3.  **Status Bar (Thanh trạng thái - Dưới cùng):** Một thanh để hiển thị thông tin liên tục như tổng số lượng thuốc và các cảnh báo quan trọng.

-   **Điều hướng (Navigation):** Sidebar nên chứa các mục sau:
    -   **Dashboard** (Bảng điều khiển - Chế độ xem mặc định)
    -   **Inventory** (Kho thuốc)
    -   **Reports** (Báo cáo - Tính năng cho tương lai)
    -   **Settings** (Cài đặt - Tính năng cho tương lai)

-   **Phím tắt (Keyboard Shortcuts):** Các phím tắt toàn cục sau đây phải được hỗ trợ:
    -   `Ctrl+K`: Mở **Global Search Modal** (Hộp thoại tìm kiếm toàn cục).
    -   `Ctrl+N`: Mở **Add Medicine Dialog** (Hộp thoại thêm thuốc).
    -   `Ctrl+D`: Chuyển đổi giữa **Light và Dark theme**.

### **2. Chế độ xem 1: Dashboard (Bảng điều khiển - Bề mặt chính)**

**Mục đích:** Cung cấp một cái nhìn tổng quan, "nhìn nhanh" về tình trạng kho thuốc. Đây là màn hình đầu tiên người dùng nhìn thấy và cần làm nổi bật ngay lập tức các thông tin quan trọng.

**Các thành phần bắt buộc:**

#### **A. Thẻ Chỉ số Hiệu suất chính (KPI Cards)**
Một bộ các thẻ tóm tắt nổi bật, dễ đọc ở đầu trang. Mỗi thẻ nên có một con số lớn và một nhãn rõ ràng.
-   **Total Inventory (Tổng kho):** Tổng số loại thuốc duy nhất.
-   **Expiring Soon (Sắp hết hạn):** Số lượng thuốc sẽ hết hạn trong vòng 30 ngày tới. Thẻ này nên có màu nhấn là **vàng**.
-   **Expired Medicines (Thuốc đã hết hạn):** Số lượng thuốc đã hết hạn. Thẻ này nên có màu nhấn là **đỏ**.
-   **Low Stock (Sắp hết hàng):** Số lượng thuốc có số lượng dưới ngưỡng quy định (ví dụ: 5 đơn vị). Thẻ này nên có màu nhấn là **cam** hoặc **vàng**.

#### **B. Biểu đồ & Trực quan hóa (Tích hợp Matplotlib)**
Bảng điều khiển sẽ có hai biểu đồ chính được nhúng trong giao diện PyQt6.

1.  **Expiry Status Distribution (Biểu đồ tròn Phân bổ Tình trạng Hạn sử dụng):**
    -   **Mục đích:** Để hiển thị tỷ lệ của kho thuốc dựa trên tình trạng hạn sử dụng.
    -   **Các phần/Dữ liệu:**
        -   `Normal` (Còn hạn): Đại diện cho các loại thuốc không hết hạn trong vòng 30 ngày. (Màu đề xuất: **Xanh lá**)
        -   `Expiring Soon` (Sắp hết hạn trong 0-30 ngày): (Màu đề xuất: **Vàng**)
        -   `Expired` (Đã hết hạn): (Màu đề xuất: **Đỏ**)
    -   **Nhãn:** Mỗi phần của biểu đồ tròn phải được dán nhãn rõ ràng với danh mục và tỷ lệ phần trăm.

2.  **Top 10 Medicines by Stock (Biểu đồ cột Top 10 thuốc tồn kho nhiều nhất):**
    -   **Mục đích:** Để nhanh chóng xác định các mặt hàng có số lượng nhiều nhất trong kho.
    -   **Trục X:** Tên thuốc.
    -   **Trục Y:** Số lượng.
    -   **Thiết kế:** Một biểu đồ cột dọc đơn giản, được sắp xếp theo thứ tự số lượng giảm dần.

#### **C. Danh sách có thể hành động (Actionable Lists)**
Hai widget danh sách/bảng nhỏ để cung cấp quyền truy cập trực tiếp vào các mục quan trọng mà không cần phải điều hướng đến chế độ xem kho đầy đủ.
1.  **Danh sách "Approaching Expiry" (Sắp hết hạn):**
    -   Hiển thị 5-10 loại thuốc gần ngày hết hạn nhất.
    -   **Các cột:** Tên thuốc, Ngày hết hạn, Số ngày còn lại.
    -   **Tương tác:** Nhấp vào một mục sẽ điều hướng đến và làm nổi bật mục đó trong `Inventory View` chính.

2.  **Danh sách "Low Stock Items" (Mặt hàng sắp hết):**
    -   Hiển thị 5-10 loại thuốc có số lượng thấp nhất.
    -   **Các cột:** Tên thuốc, Số lượng, Vị trí trên kệ.
    -   **Tương tác:** Nhấp vào một mục sẽ điều hướng đến và làm nổi bật mục đó trong `Inventory View` chính.

#### **D. Điều khiển (Controls)**
-   **Nút Refresh:** Một nút để tải lại toàn bộ dữ liệu và biểu đồ trên dashboard theo cách thủ công.

---

### **3. Chế độ xem 2: Quản lý Kho (Inventory Management)**

**Mục đích:** Không gian làm việc chính để xem, thêm, chỉnh sửa và xóa các bản ghi thuốc.

**Các thành phần bắt buộc:**

-   **Thành phần chính:** Một bảng đầy đủ tính năng (`QTableView`).
-   **Các cột của bảng:** Bảng phải hiển thị:
    -   `Name` (Tên)
    -   `Quantity` (Số lượng)
    -   `Expiry Date` (Ngày hết hạn)
    -   `Shelf` (ID Vị trí kệ)
    -   `Price` (Giá)
    -   `Status` (Trạng thái - một trường được suy ra, ví dụ: "Hết hạn", "Sắp hết hàng")
-   **Sắp xếp & Lọc:** Tất cả các cột phải có thể sắp xếp được. Cần có một thanh tìm kiếm/lọc phía trên bảng để lọc theo tên.
-   **Định dạng có điều kiện (Conditional Formatting):** Các hàng của bảng phải được tô màu để nhận dạng nhanh:
    -   **Hàng màu đỏ:** Thuốc đã hết hạn.
    -   **Hàng màu vàng:** Thuốc sắp hết hạn (trong vòng 30 ngày).
    -   **Hàng mặc định:** Tình trạng bình thường.
-   **Tương tác:**
    -   **Nhấp đúp chuột** vào một hàng sẽ mở **Edit Medicine Dialog** (Hộp thoại sửa thuốc) cho mục đó.
    -   **Nhấp chuột phải** vào một hàng sẽ mở một menu ngữ cảnh với các tùy chọn `Edit` (Sửa) và `Delete` (Xóa).
    -   Một nút **"Add Medicine"** (Thêm thuốc) (biểu tượng `+`) nên có mặt trên chế độ xem này để mở Add Medicine Dialog.

---

### **4. Thành phần: Hộp thoại Thêm/Sửa thuốc (Add/Edit Medicine Dialog)**

**Mục đích:** Một form dạng modal (`QDialog`) để nhập liệu.

**Các trường bắt buộc:**
-   **Name (Tên):** `QLineEdit`
-   **Quantity (Số lượng):** `QSpinBox` (chỉ nhận giá trị không âm).
-   **Expiry Date (Ngày hết hạn):** `QDateEdit` với lịch bật lên.
-   **Shelf (Kệ):** `QComboBox` được điền dữ liệu từ các vị trí kệ có sẵn.
-   **Price (Giá):** `QLineEdit` hoặc `QDoubleSpinBox`.
-   **Nút:** `Save` (Lưu) và `Cancel` (Hủy). Nút `Save` phải bị vô hiệu hóa cho đến khi tất cả các trường bắt buộc đều hợp lệ.

---

### **5. Thành phần: Hộp thoại Tìm kiếm Toàn cục (Global Search Modal)**

**Mục đích:** Một công cụ tìm kiếm nhanh trên toàn hệ thống, có thể truy cập từ bất kỳ đâu qua `Ctrl+K`.

**Các thành phần bắt buộc:**
-   **Bố cục:** Một hộp thoại modal đơn giản, không chặn (`QDialog`) với một `QLineEdit` duy nhất ở trên cùng và một `QListWidget` ở dưới.
-   **Hành vi:**
    -   Khi người dùng gõ vào `QLineEdit`, `QListWidget` sẽ ngay lập tức cập nhật với các kết quả tìm kiếm mờ (fuzzy search).
    -   Mỗi mục kết quả nên hiển thị **Tên thuốc** và **điểm số khớp** (ví dụ: "Paracetamol 500mg (95%)").
    -   Chọn một kết quả từ danh sách sẽ đóng hộp thoại, chuyển chế độ xem chính sang **Inventory**, và làm nổi bật loại thuốc đã chọn trong bảng.
