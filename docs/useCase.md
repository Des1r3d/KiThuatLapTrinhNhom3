# Đặc tả Use Case: Phần mềm quản lý kho thuốc y tế

Dưới đây là các bảng đặc tả chi tiết cho các Use Case phân rã của phần mềm quản lý kho thuốc y tế, dựa theo sơ đồ chức năng.

## Nhóm chức năng Quản lý danh mục Thuốc

### 1. Đặc tả UC: Thêm thuốc
| **UC – Thêm thuốc** | |
| --- | --- |
| **Tên** | Thêm thuốc mới |
| **Mô tả** | Chức năng cho phép người dùng khai báo thông tin của một loại thuốc mới vào hệ thống quản lý. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Ứng dụng đã khởi động ưu tiên tính năng tự tạo file dữ liệu lưu trữ thuốc trống (blank file) nếu chạy lần đầu. Yêu cầu cần có sẵn dữ liệu kệ hàng khả dụng để định vị chỗ chứa trước. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng chuyển sang màn hình Inventory và bấm "Thêm thuốc".<br>Bước 2: Hệ thống hiển thị form điền thông tin thuốc (Tên, số lượng, giá, HSD, kệ đích...).<br>Bước 3: Người dùng điền đầy đủ thông tin hợp lệ và bấm "Lưu".<br>Bước 4: Hệ thống xác thực sức chứa của kệ, nếu hợp lệ thì ghi nhận dữ liệu xuống tệp.<br><br>**Luồng sự kiện phụ**<br>(4A): Nếu dữ liệu không hợp lệ (để trống, sai định dạng) hoặc vị trí kệ đích đã đầy, hệ thống xuất thông báo lỗi không cho phép lưu tiếp. |
| **Điều kiện sau** | Dữ liệu thuốc mới được lưu và danh sách tự động tải lại hiện sản phẩm mới thêm. |

### 2. Đặc tả UC: Sửa thông tin thuốc
| **UC – Sửa thông tin thuốc** | |
| --- | --- |
| **Tên** | Sửa thông tin thuốc |
| **Mô tả** | Cập nhật lại các thông tin sai sót hoặc biến động (chỉnh sửa số lượng, đổi kệ, sửa giá). |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Tìm kiếm thuốc |
| **Điều kiện tiên quyết** | Thuốc cần chỉnh sửa phải tồn tại sẵn trong phần mềm. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng chọn 1 loại thuốc trong bảng danh sách (có thể qua tìm kiếm) và bấm "Sửa".<br>Bước 2: Hệ thống load form chứa sẵn các thông tin cũ của loại thuốc đó.<br>Bước 3: Người dùng thao tác chỉnh sửa thông tin cần thay đổi và bấm "Lưu".<br>Bước 4: Hệ thống kiểm tra hợp lệ và tiến hành cập nhật vào file lưu trữ.<br><br>**Luồng sự kiện phụ**<br>(4A): Dữ liệu sau chỉnh sửa không qua được vòng xác thực (ví dụ kệ đích không đủ chỗ trống), hệ thống báo lỗi không thành công. |
| **Điều kiện sau** | Nội dung thông tin được lưu ghi đè thành công và giao diện được refresh lại ngay lập tức. |

### 3. Đặc tả UC: Xóa thuốc
| **UC – Xóa thuốc** | |
| --- | --- |
| **Tên** | Xóa thuốc khỏi kho |
| **Mô tả** | Xóa hoàn toàn bản ghi của một loại thuốc không còn kinh doanh hoặc hết mã ra khỏi kho lưu trữ. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Tìm kiếm thuốc |
| **Điều kiện tiên quyết** | Xác thực sản phẩm thuốc đang nằm trong hệ thống. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng tìm và chọn loại thuốc cần loại bỏ, sau đó bấm "Xóa".<br>Bước 2: Hệ thống bật cửa sổ Popup cảnh báo xác nhận có chắc chắn muốn xóa không.<br>Bước 3: Người dùng bấm "Đồng ý".<br>Bước 4: Hệ thống xử lý giải phóng không gian trên kệ và gỡ bỏ dữ liệu trong file lưu trữ.<br><br>**Luồng sự kiện phụ**<br>(3A): Người dùng ấn "Hủy" hoặc đóng pop-up, hệ thống trở về trạng thái cũ không đổi. |
| **Điều kiện sau** | Thuốc bị gỡ dữ liệu vĩnh viễn và không còn xuất hiện trên màn hình quản lý. Sức chứa kệ hàng được cập lại phần không gian trống. |

### 4. Đặc tả UC: Xem chi tiết thuốc
| **UC – Xem chi tiết thuốc** | |
| --- | --- |
| **Tên** | Xem chi tiết thuốc |
| **Mô tả** | Liệt kê màn hình tóm tắt thông tin đầy đủ nhất về thuốc, mã số định danh, cảnh báo hết hạn đối với mặt hàng đó. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Tìm kiếm thuốc |
| **Điều kiện tiên quyết** | Hệ thống đang hiển thị giao diện danh sách hàng hoặc thanh Search. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng double-click hoặc ấn "Xem chi tiết" vào mục một loại thuốc nhất định.<br>Bước 2: Hệ thống tải UI "Medicine Detail" thống kê toàn bộ quy cách, vị trí kệ và ảnh (nếu có).<br>Bước 3: Người dùng xem và có thể đóng cửa sổ lại.<br><br>**Luồng sự kiện phụ**<br>Không có. |
| **Điều kiện sau** | Không làm biến đổi dữ liệu, hệ thống vẫn duy trì ở trạng thái đọc. |

---

## Nhóm chức năng Quản lý Kệ hàng

### 5. Đặc tả UC: Thêm kệ hàng
| **UC – Thêm kệ hàng** | |
| --- | --- |
| **Tên** | Thêm kệ hàng mới |
| **Mô tả** | Thiết lập không gian lưu trữ vật lý mới cho hệ thống nhận diện. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Phần mềm mở đúng ở giao diện Quản lý Kệ (Shelf View). Nếu đây là lần chạy mới hoàn toàn, hệ thống tự động khởi tạo file dữ liệu kệ hàng trống (blank file). |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng nhấn "Thêm kệ".<br>Bước 2: Hệ thống hiện form tạo khối. Người dùng nhập Dãy/Column, Hàng/Row và Sức chứa (Capacity). Ô Khu vực (Zone) bị khoá không được tương tác do hệ thống tự động tạo (auto-generate) dựa trên Dãy/Cột nhập vào.<br>Bước 3: Người dùng ấn "Lưu".<br>Bước 4: Hệ thống lưu kệ mới vào kho lưu trữ.<br><br>**Luồng sự kiện phụ**<br>(4A): Dữ liệu truyền vào sai định dạng số hoặc chuỗi cấm, ngăn chặn và báo lỗi yêu cầu chỉnh lại. |
| **Điều kiện sau** | Cập nhật kho dữ liệu có kệ mới hiển thị ở UI và có thể sẵn sàng chứa thuốc thêm vào. |

### 6. Đặc tả UC: Sửa kệ hàng
| **UC – Sửa kệ hàng** | |
| --- | --- |
| **Tên** | Sửa thông tin kệ hàng |
| **Mô tả** | Nhằm thay đổi sức chứa của kệ hoặc đổi tên vị trí cột/hàng của kệ khi cơ sở kho được trùng tu. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Kệ đó đã được khai báo trên hệ thống. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng chọn 1 kệ đang có và bấm "Sửa".<br>Bước 2: Form giữ lại thông số cũ và cho phép Edit các ô Cột/Hàng/Sức chứa (Khu vực/Zone vẫn bị khoá tự đổi nếu Cột/Hàng thay đổi).<br>Bước 3: Người dùng sửa xong và bấm "Lưu".<br>Bước 4: Trình quản lý nạp dữ liệu đè lên kệ tương ứng ở tệp gốc.<br><br>**Luồng sự kiện phụ**<br>(4A): Nếu sửa "Sức chứa tối đa (Capacity)" mới lại NHỎ HƠN tổng số lượng thuốc hiện đang để trên đó, hệ thống báo lỗi không hợp lệ bắt buộc xuất bớt thuốc ra. |
| **Điều kiện sau** | Dữ kiện vật lý về kệ được cập nhật trên bảng. |

### 7. Đặc tả UC: Xóa kệ hàng
| **UC – Xóa kệ hàng** | |
| --- | --- |
| **Tên** | Xóa kệ hàng |
| **Mô tả** | Hủy bỏ thông tin của kệ hàng khỏi kho khi kệ bị dỡ bỏ. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Kệ hàng tồn tại trên hệ thống. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Nhấn chọn và "Xóa kệ".<br>Bước 2: Popup cảnh báo sự mất mát.<br>Bước 3: Người dùng xác nhận rủi ro.<br>Bước 4: Server tiếp nhận lệnh xóa từ UI để diệt đối tượng kệ trong data list.<br><br>**Luồng sự kiện phụ**<br>(4A): Hệ thống chặn luồng xóa nểu phát hiện trên Kệ đang CÒN CHỨA THUỐC. Cảnh báo hiển thị người dùng phải chuyển các thuốc sang kệ khác trước khi tiến hành xóa kệ. |
| **Điều kiện sau** | Danh sách kệ trống chỗ dòng liên hệ vừa xóa. |

---

## Các chức năng khác

### 8. Đặc tả UC: Tìm kiếm thuốc
| **UC – Tìm kiếm thuốc** | |
| --- | --- |
| **Tên** | Tìm kiếm thuốc (Global Search) |
| **Mô tả** | Công cụ tra cứu sản phẩm dựa theo keyword nhanh chóng mọi lúc mọi nơi bằng Fuzzy logic. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Kho thuốc sở hữu ít nhất 1 mặt hàng. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Ấn Ctrl+K / click vào Search box.<br>Bước 2: Nhập từ khoá.<br>Bước 3: Module search tự lo việc lọc thông minh (Fuzzy) và show chuỗi kết quả trùng khớp ngay lập tức.<br>Bước 4: Người dùng chọn vào đúng món mình tìm, hệ thống auto chuyển về màn hình "Xem chi tiết thuốc".<br><br>**Luồng sự kiện phụ**<br>(3A): Trả về bảng trắng ghi chữ "Không có kết quả". |
| **Điều kiện sau** | Hệ thống chuyển view đến màn thông tin cụ thể món hàng. |

### 9. Đặc tả UC: Xem cảnh báo hệ thống
| **UC – Xem cảnh báo hệ thống** | |
| --- | --- |
| **Tên** | Xem cảnh báo hệ thống |
| **Mô tả** | Tính năng Audit kho, rà soát hạn sử dụng (cận date/đã hết) và ngưỡng tồn kho thấp/cạn kiệt. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Không có yêu cầu. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Thuật toán AlertSystem chạy nền đánh giá mọi loại thuốc.<br>Bước 2: Hiển thị giao diện báo động trên Notification list (khu Dashboard).<br>Bước 3: User click vô mục cảnh báo.<br>Bước 4: Pop-up danh sách các loại thuốc gặp trạng thái xấu.<br><br>**Luồng sự kiện phụ**<br>(1A): Hệ thống đánh giá không có vi phạm, để trạng thái im lặng "Hoạt động bình thường". |
| **Điều kiện sau** | User nắm được thông tin lô hàng kém để có biện pháp xử lý. |

### 10. Đặc tả UC: Tùy chỉnh giao diện
| **UC – Tùy chỉnh giao diện** | |
| --- | --- |
| **Tên** | Tùy chỉnh giao diện (Đổi Theme Sáng/Tối) |
| **Mô tả** | Đổi màu toàn bộ cửa sổ sang giao diện màu xám tối và ngược lại bảo vệ mắt cho các khoảng ca trực. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Main window đang hiển thị bình thường. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Quản trị viên click vào Toggle Mode (Sáng/Tối).<br>Bước 2: Nhớ lại bộ chỉ mục của View hiện hành đang mở.<br>Bước 3: Call hàm thay đổi theme StyleSheet (Tối hoặc Sáng) cho toàn cục Widget.<br>Bước 4: Layout nháy lên Reload mà vẫn duy trì ở vị trí nội dung làm việc ban nãy.<br><br>**Luồng sự kiện phụ**<br>Không có. |
| **Điều kiện sau** | Mọi thành phần khung cửa có tông màu mới, trải nghiệm dùng phần mềm ổn định. |
