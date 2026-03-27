# Đặc tả Use Case: Phần mềm quản lý kho thuốc y tế

Dưới đây là các bảng đặc tả chi tiết cho 5 Use Case chính của phần mềm quản lý kho thuốc y tế, dựa trên sơ đồ chức năng.

## 1. Đặc tả UC: Quản lý danh mục Thuốc

| **UC – Quản lý danh mục Thuốc** | |
| --- | --- |
| **Tên** | Quản lý danh mục Thuốc |
| **Mô tả** | Cho phép người dùng thêm mới, chỉnh sửa, xóa và xem chi tiết thông tin thuốc trong kho quản lý. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Tìm kiếm thuốc |
| **Điều kiện tiên quyết** | Ứng dụng đã được khởi động, có sẵn file lưu trữ thông tin thuốc hợp lệ. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng chọn chức năng Quản lý danh mục thuốc.<br>Bước 2: Hệ thống tải danh sách toàn bộ các loại tự động.<br>Bước 3: Người dùng nhấn các nút thao tác tương ứng (Thêm, Sửa, Xóa, Xem chi tiết).<br>Bước 4: Hệ thống mở popup hoặc form nhập thông tin, biểu đồ dữ liệu tương ứng.<br>Bước 5: Người dùng bấm Lưu (hoặc Xác nhận xóa). Hệ thống ghi dữ liệu vào hệ thống.<br><br>**Luồng sự kiện phụ**<br>(5A) Thay vì lưu thành công, nếu thông tin bị bỏ trống hoặc sai định dạng (v.d: số lượng âm), hệ thống chặn lại và bắt buộc chỉnh sửa lại form điền. |
| **Điều kiện sau** | Dữ liệu thuốc được ghi nhận hoàn tất ở kho lưu trữ. Hệ thống tự động tải lại màn hình hiển thị danh mục mới nhất. |

## 2. Đặc tả UC: Quản lý Kệ hàng

| **UC – Quản lý Kệ hàng** | |
| --- | --- |
| **Tên** | Quản lý Kệ hàng |
| **Mô tả** | Quản trị khu vực sắp xếp: tạo mới chức năng, quản lý và theo dõi sức chứa của các kệ để thuốc. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Ứng dụng hoạt động bình thường, ở chức năng xem kệ hiện tại (Shelf View). |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng chuyển qua tab quản lý Kệ hàng.<br>Bước 2: Hệ thống hiện danh sách kệ kèm theo thống kê sức chứa khả dụng.<br>Bước 3: Người dùng chọn Thêm Kệ hoặc Sửa/Xóa.<br>Bước 4: Người dùng nhập các thông số định nghĩa cho mã kệ (Khu vực, Cột, Hàng, Sức chứa lượng thuốc).<br>Bước 5: Người dùng yêu cầu lưu, hệ thống xác nhận thiết lập kệ.<br><br>**Luồng sự kiện phụ**<br>(5A): Khi nhập lượng thuốc mới lên kệ, nếu không đủ sức chứa do kệ vượt quá hạn định (Capacity), phần mềm hiện thông báo yêu cầu chuyển kệ. |
| **Điều kiện sau** | Dữ liệu kệ hàng được lưu và thông tin dung lượng vị trí kho được cập nhật lên giao diện chính. |

## 3. Đặc tả UC: Tìm kiếm thuốc

| **UC – Tìm kiếm thuốc** | |
| --- | --- |
| **Tên** | Tìm kiếm thuốc (Global Search) |
| **Mô tả** | Chức năng tìm nhanh thuốc giúp người dùng dễ dàng truy ra loại thuốc mình muốn từ mọi màn hình ứng dụng thông qua từ khóa (hỗ trợ tìm mờ). |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Đã có sẵn dữ liệu và hệ thống đã Index thông tin. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Người dùng nhấp vào thanh tìm kiếm trên cùng hoặc gọi tắt bằng phím (Ctrl+K).<br>Bước 2: Người dùng gõ tên sản phẩm thuốc.<br>Bước 3: Ở thời gian thực, hệ thống kích hoạt module Fuzzy Search, lọc tên sát tự động tạo danh sách gợi ý đổ xuống.<br>Bước 4: Người dùng tham chiếu dòng kết quả, click thẳng vào và hệ thống tự điều hướng qua Xem chi tiết loại thuốc đó.<br><br>**Luồng sự kiện phụ**<br>(3A): Từ khóa gõ bị sai lệch lớn không có kết quả hợp lệ, hiển thị cảnh báo "Khôn tìm thấy". |
| **Điều kiện sau** | Người dùng xem được chính xác chi tiết dữ liệu về loại hàng/thuốc theo mình mong muốn. |

## 4. Đặc tả UC: Xem cảnh báo hệ thống

| **UC – Xem cảnh báo hệ thống** | |
| --- | --- |
| **Tên** | Xem cảnh báo hệ thống |
| **Mô tả** | Chẩn đoán các báo cáo rủi ro hàng ngày, cung cấp list các thuốc tình trạng đặc biệt (Sắp/đã hết hạn hoặc trạng thái cạn hàng). |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Thuốc đã được đăng ký thời gian hạn sử dụng và số lượng tồn vào kho lưu trữ. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Hệ thống tự động đọc tập tin dữ liệu và nhận định hạn mức (Threshold) rủi ro được cài đặt.<br>Bước 2: Nhóm các cảnh báo vi phạm, ưu tiên màu cho Dashboard / Notification bar.<br>Bước 3: Người dùng xem biểu tượng hay mục báo cáo.<br>Bước 4: Hệ thống pop-up chi tiết danh sách mặt hàng, ngày còn lại cũng như lô sắp hết.<br><br>**Luồng sự kiện phụ**<br>(1A): Ở bước 1 & 2 nếu tất cả nằm ở độ an toàn: hệ thống tắt hoặc ghi chú "Trạng thái hiển hành bình ổn". |
| **Điều kiện sau** | Cung cấp thông tin kịp thời để người quản lý biết để luân chuyển hoặc đặt hàng kho chuẩn. |

## 5. Đặc tả UC: Tùy chỉnh giao diện

| **UC – Tùy chỉnh giao diện** | |
| --- | --- |
| **Tên** | Tùy chỉnh giao diện (Theme Sáng/Tối) |
| **Mô tả** | Thao tác đổi mode giao diện cho việc kiểm tra trải nghiệm sáng/tối dễ chịu theo ca làm ca đêm/ngày. |
| **Actors** | User (Quản lý kho/Dược sĩ) |
| **Includes** | Không có |
| **Extends** | Không có |
| **Điều kiện tiên quyết** | Phần mềm hoạt động ở giao diện đồ hoạ. |
| **Luồng sự kiện** | **Luồng sự kiện chính**<br>Bước 1: Từ màn hình chính người dùng bấm công tắc Đổi theme Sáng (Light) / Tối (Dark).<br>Bước 2: Hệ thống sao lưu chỉ mục trang đang dừng tại thời điểm đó.<br>Bước 3: Trình điều hướng chạy tệp file giao diện Dark hoặc Light đã Compile lên màn hình.<br>Bước 4: Reload giao diện toàn phần giữ lại ngay giao diện vừa click (Tức là trạng thái màn tiếp theo vẫn nằm ở Tab đấy).<br><br>**Luồng sự kiện phụ**<br>Không có. |
| **Điều kiện sau** | Toàn bộ các mảng màu đều hoàn thiện cập nhật thay đổi theo chủ đề yêu thích mà các chức năng vận trơn tru. |
