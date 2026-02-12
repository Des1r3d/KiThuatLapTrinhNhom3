# Hướng dẫn Thiết kế UX/UI: Hệ thống Quản lý Kho Thuốc (Phiên bản Beta)

Tài liệu này cung cấp các hướng dẫn thiết kế UX/UI cốt lõi cho phiên bản Beta của Hệ thống Quản lý Kho Thuốc, nhằm giúp đội ngũ thiết kế nắm bắt rõ ràng phạm vi, các quy tắc và kỳ vọng cho giai đoạn phát triển hiện tại.

---

## 1. Tổng quan Sản phẩm (Product Overview)

Tài liệu này cung cấp hướng dẫn thiết kế UX/UI cho phiên bản Beta của Hệ thống Quản lý Kho Thuốc, tập trung vào các chức năng cốt lõi và giới hạn phạm vi cho giai đoạn thử nghiệm ban đầu.

*   **Ứng dụng dành cho:** Các **Dược sĩ** (Pharmacist) làm việc tại nhà thuốc hoặc cơ sở y tế, những người cần công cụ để quản lý hàng tồn kho thuốc.
*   **Vấn đề giải quyết:**
    *   Khó khăn trong việc theo dõi chính xác số lượng thuốc tồn kho.
    *   Rủi ro bán hoặc sử dụng thuốc hết hạn.
    *   Thời gian tìm kiếm thuốc thủ công tốn kém.
    *   Thiếu thông tin tổng quan nhanh về tình trạng kho.
*   **Các tính năng có trong phiên bản Beta:**
    *   Quản lý thông tin thuốc cơ bản (thêm, sửa, xóa).
    *   Cảnh báo về thuốc sắp hết hạn và tồn kho thấp/hết hàng.
    *   Tìm kiếm thuốc nhanh chóng và linh hoạt.
    *   Giao diện người dùng trực quan, hỗ trợ chế độ Sáng/Tối.
*   **Các tính năng CHƯA bao gồm trong phiên bản Beta:**
    *   Phân quyền người dùng chi tiết (quản lý vai trò).
    *   Chức năng báo cáo nâng cao và tùy chỉnh.
    *   Đồng bộ hóa dữ liệu trên nền tảng đám mây.
    *   Tối ưu hóa hiệu suất cho cơ sở dữ liệu rất lớn (>10.000 bản ghi).

---

## 2. Phạm vi Tính năng (Phiên bản Beta)

Bảng dưới đây liệt kê các tính năng chính có trong phiên bản Beta, cùng với trạng thái hiện tại và ghi chú liên quan đến thiết kế UX/UI.

| Tính năng          | Trạng thái | Ghi chú                                   |
| :---------------- | :-------- | :---------------------------------------- |
| **Quản lý Thuốc** |           |                                           |
| Thêm thuốc mới     | Hoạt động | Có xác thực dữ liệu đầu vào.              |
| Sửa thông tin thuốc | Hoạt động | Cho phép cập nhật các trường trừ ID.     |
| Xóa thuốc         | Hoạt động | Yêu cầu xác nhận trước khi xóa.           |
| **Giám sát & Cảnh báo** |           |                                           |
| Dashboard         | Cơ bản    | Hiển thị tóm tắt cảnh báo, chưa có biểu đồ nâng cao. |
| Cảnh báo hết hạn  | Hoạt động | Các loại cảnh báo: hết hạn, sắp hết hạn, tồn kho thấp, hết hàng. |
| **Tìm kiếm**      |           |                                           |
| Tìm kiếm toàn cục | Hoạt động | Hỗ trợ tìm kiếm mờ (fuzzy search).        |
| **Giao diện**     |           |                                           |
| Chế độ Sáng/Tối   | Có        | Hỗ trợ chuyển đổi giữa Light và Dark mode. |

---

## 3. Luồng Người dùng Chính (High-Level User Flows)

Phần này tóm tắt các luồng thao tác chính của người dùng, giúp designer nắm bắt bức tranh tổng thể về các tương tác cơ bản.

*   **Thêm thuốc:** Mở hộp thoại -> Điền thông tin -> Xác thực -> Lưu -> Cập nhật hiển thị.
*   **Sửa thuốc:** Chọn thuốc từ bảng -> Mở hộp thoại sửa -> Chỉnh sửa thông tin -> Xác thực -> Lưu -> Cập nhật hiển thị.
*   **Xóa thuốc:** Chọn thuốc từ bảng -> Nhấn xóa -> Xác nhận -> Xóa -> Cập nhật hiển thị.
*   **Tìm kiếm:** Nhấn phím tắt `Ctrl+K` -> Mở thanh tìm kiếm -> Nhập từ khóa -> Hiển thị kết quả mờ -> Chọn kết quả -> Xem chi tiết/vị trí.
*   **Xử lý cảnh báo:** Xem tóm tắt cảnh báo trên Dashboard -> Điều hướng đến Inventory để kiểm tra chi tiết thuốc bị cảnh báo -> Thực hiện hành động phù hợp (ví dụ: sửa hạn dùng, bổ sung hàng).

---

## 4. Quy tắc Nghiệp vụ ảnh hưởng đến UI (Business Rules ảnh hưởng đến UI)

Phần này mô tả các quy tắc nghiệp vụ cốt lõi có tác động trực tiếp đến cách UI cần được thiết kế và hành xử.

*   **Chỉnh sửa/Xóa thuốc hết hạn:**
    *   Hệ thống có thể cho phép chỉnh sửa thông tin của thuốc đã hết hạn (ví dụ: nếu phát hiện sai sót trong nhập liệu) nhưng cần có cảnh báo trực quan mạnh mẽ trên UI về trạng thái hết hạn của thuốc.
    *   Thao tác xóa thuốc đã hết hạn nên được cho phép, nhưng cần một hộp thoại xác nhận rõ ràng.
*   **Xóa thuốc đang tồn kho:**
    *   Khi người dùng cố gắng xóa một loại thuốc mà `Số lượng > 0`, UI phải hiển thị một hộp thoại xác nhận mạnh mẽ (`QMessageBox.question`) với thông báo rõ ràng (ví dụ: "Bạn có chắc chắn muốn xóa thuốc '[Tên Thuốc]' hiện đang còn [X] đơn vị trong kho? Thao tác này không thể hoàn tác.").
*   **Giới hạn số lượng:**
    *   Về mặt nghiệp vụ, hệ thống không áp đặt giới hạn cứng về `Số lượng` tối đa. Tuy nhiên, nếu người dùng nhập một giá trị `Số lượng` cực lớn (ví dụ: > 9999), UI có thể hiển thị một cảnh báo nhẹ nhàng để người dùng xác nhận lại đầu vào, đảm bảo không có lỗi nhập liệu.
*   **Xác nhận khi xóa:**
    *   Mọi thao tác xóa (ví dụ: xóa thuốc, xóa kệ) cần một hộp thoại xác nhận rõ ràng và yêu cầu người dùng xác nhận lại trước khi thực hiện, để tránh mất dữ liệu không mong muốn.

---

## 5. Trạng thái UI và các Trường hợp Biên (UI States & Edge Cases)

Phần này mô tả cách giao diện người dùng nên phản ứng trong các điều kiện khác nhau và cách xử lý các tình huống bất ngờ hoặc không mong muốn.

### 5.1. Trạng thái UI (UI States)

*   **Trạng thái Tải (Loading State):**
    *   **Khi nào:** Khi ứng dụng khởi động, tải dữ liệu lớn, hoặc thực hiện một thao tác mất thời gian (ví dụ: lưu dữ liệu).
    *   **UI phản hồi:** Hiển thị một chỉ báo tải rõ ràng (ví dụ: `QProgressBar`, `QProgressDialog`, hoặc biểu tượng spinner). Các thành phần tương tác chính có thể bị vô hiệu hóa (`setEnabled(False)`) để ngăn chặn đầu vào không mong muốn.
*   **Trạng thái Rỗng (Empty State):**
    *   **Khi nào:** Không có thuốc nào trong kho (`InventoryView`) hoặc kết quả tìm kiếm trống.
    *   **UI phản hồi:** Thay vì hiển thị bảng trống, hiển thị một thông báo thân thiện ở trung tâm khu vực hiển thị (ví dụ: "Không tìm thấy thuốc nào. Vui lòng nhấp 'Thêm thuốc mới' để bắt đầu.") và có thể hiển thị một biểu tượng minh họa. Các nút "Chỉnh sửa" hoặc "Xóa" nên bị vô hiệu hóa.
*   **Trạng thái Thành công (Success State):**
    *   **Khi nào:** Sau một thao tác hoàn tất thành công (ví dụ: thêm, cập nhật, xóa thuốc).
    *   **UI phản hồi:** Hiển thị thông báo ngắn gọn, không xâm lấn trên thanh trạng thái (`QStatusBar`) hoặc một `QMessageBox` tự động biến mất sau vài giây.
*   **Trạng thái Lỗi (Error State):**
    *   **Khi nào:** Một lỗi xảy ra (ví dụ: lỗi xác thực, lỗi hệ thống, lỗi lưu trữ).
    *   **UI phản hồi:** Hiển thị thông báo lỗi rõ ràng và có thể hành động được. Đối với lỗi nghiêm trọng, sử dụng `QMessageBox` với mô tả lỗi và các bước khắc phục được đề xuất. Đối với lỗi xác thực, phản hồi trực tiếp tại trường nhập liệu.
*   **Trạng thái Vô hiệu hóa (Disabled State):**
    *   **Khi nào:** Các chức năng hoặc nút không khả dụng trong ngữ cảnh hiện tại (ví dụ: nút "Xóa" khi không có thuốc nào được chọn, nút "Lưu" khi dữ liệu không hợp lệ).
    *   **UI phản hồi:** Thành phần bị làm mờ hoặc chuyển sang màu xám (`setEnabled(False)`) và có thể có một tooltip giải thích lý do không khả dụng.
*   **Trạng thái Sắp hết hạn/Hết hạn/Tồn kho thấp (Expiring/Expired/Low Stock State):**
    *   **Khi nào:** Thuốc đạt đến các ngưỡng cảnh báo (`AlertSystem`).
    *   **UI phản hồi:** Trong `InventoryView` (`QTableView`), các hàng thuốc tương ứng được mã hóa màu (ví dụ: đỏ cho hết hạn, vàng cho sắp hết hạn, cam cho tồn kho thấp). `Dashboard` hiển thị tóm tắt cảnh báo với số lượng rõ ràng, có thể có biểu tượng cảnh báo.

### 5.2. Các Trường hợp Biên (Edge Cases)

*   **Không tìm thấy tệp dữ liệu / Tệp dữ liệu bị hỏng:**
    *   **Tình huống:** Lớp `StorageEngine` không tìm thấy tệp `medicines.json` hoặc `shelves.json`, hoặc tệp bị hỏng (`json.JSONDecodeError`).
    *   **UI phản hồi:**
        *   Nếu có bản sao lưu, hệ thống sẽ cố gắng khôi phục và hiển thị cảnh báo cho người dùng (ví dụ: "Dữ liệu kho chính bị hỏng, đã khôi phục từ bản sao lưu.").
        *   Nếu không có bản sao lưu hoặc cả hai đều hỏng, ứng dụng sẽ khởi động với kho trống và thông báo rõ ràng cho người dùng (ví dụ: "Không tìm thấy dữ liệu kho hoặc dữ liệu bị hỏng. Đã khởi tạo kho trống.").
*   **Lỗi ghi tệp (`StorageEngine`):**
    *   **Tình huống:** Không thể lưu thay đổi vào đĩa (ví dụ: không đủ dung lượng ổ đĩa, lỗi quyền truy cập).
    *   **UI phản hồi:** Hiển thị một `QMessageBox` lỗi nghiêm trọng, giải thích vấn đề và khuyến nghị các bước khắc phục (ví dụ: "Không thể lưu dữ liệu. Vui lòng kiểm tra dung lượng ổ đĩa hoặc quyền truy cập tệp và thử lại."). Ứng dụng sẽ cố gắng giữ trạng thái dữ liệu trước đó trong bộ nhớ.
*   **Đầu vào không hợp lệ (Invalid Input - `InventoryManager`):**
    *   **Tình huống:** Người dùng nhập các giá trị không tuân thủ quy tắc nghiệp vụ (ví dụ: số lượng âm, giá âm, định dạng ngày sai, ID kệ không tồn tại).
    *   **UI phản hồi:** Cung cấp phản hồi xác thực trực tiếp tại trường nhập liệu (ví dụ: viền đỏ, tooltip, `QLabel` cảnh báo nhỏ). Ngăn không cho hành động "Lưu" cho đến khi lỗi được khắc phục.
*   **ID thuốc trùng lặp (Duplicate Medicine ID - `InventoryManager`):**
    *   **Tình huống:** Người dùng cố gắng thêm một loại thuốc mới với một ID đã tồn tại trong kho.
    *   **UI phản hồi:** Hiển thị thông báo lỗi rõ ràng trong hộp thoại "Thêm thuốc" (ví dụ: "ID thuốc này đã tồn tại. Vui lòng nhập ID khác hoặc để trống để tự động tạo ID mới."). Có thể cung cấp một nút để tự động tạo ID mới.
*   **Không có kết quả tìm kiếm (`SearchEngine`):**
    *   **Tình huống:** `SearchEngine` không tìm thấy bất kỳ loại thuốc nào khớp với truy vấn của người dùng (dưới ngưỡng `match_threshold`).
    *   **UI phản hồi:** Trong cửa sổ tìm kiếm hoặc kết quả, hiển thị thông báo "Không tìm thấy kết quả phù hợp. Vui lòng thử từ khóa khác."
*   **Số lượng thuốc lớn:**
    *   **Tình huống:** Hệ thống cần xử lý và hiển thị hàng ngàn loại thuốc trong `InventoryView`.
    *   **UI phản hồi:** Đảm bảo `QTableView` có hiệu suất tốt với `model/view architecture` và có các tính năng phân trang, sắp xếp, lọc hiệu quả.
*   **Không có kệ nào được định nghĩa:**
    *   **Tình huống:** Danh sách kệ trống khi người dùng cố gắng thêm thuốc.
    *   **UI phản hồi:** `QComboBox` cho kệ có thể hiển thị một thông báo như "Chưa có kệ nào" và vô hiệu hóa việc thêm thuốc cho đến khi ít nhất một kệ được thêm. Có thể có một nút hoặc liên kết để "Thêm kệ mới".

### 5.3. Luồng sử dụng chính (Ví dụ: Thêm thuốc)

*   Người dùng nhấp vào nút "Thêm thuốc" (thường là một `QPushButton` trong `MainWindow`).
*   Một hộp thoại `AddMedicineDialog` (một thể hiện của `QDialog`) xuất hiện.
*   Người dùng điền các trường (`QLineEdit`, `QSpinBox`, `QDateEdit`, `QComboBox`).
    *   Quá trình xác thực đầu vào diễn ra (ví dụ: kiểm tra giá trị hợp lệ trước khi đóng `QDialog`).
*   Khi lưu (nhấn `QPushButton` "Lưu"), thuốc mới được thêm vào, dữ liệu được lưu trữ và `InventoryView` được cập nhật tự động (thông qua cơ chế tín hiệu/khe cắm của Qt để cập nhật `QTableView`).

---

## 6. Hệ thống Màu sắc và Quy tắc Hình ảnh (Dành cho phiên bản Beta)

Hệ thống màu được thiết kế theo tiêu chí:
*   **Calm (dịu mắt):** Đảm bảo người dùng có thể làm việc lâu dài mà không bị mỏi mắt.
*   **Professional (chuyên nghiệp):** Phù hợp với môi trường dược/y tế, tránh các màu sắc quá rực rỡ hoặc không nghiêm túc.
*   **Hiệu quả:** Màu sắc cảnh báo rõ ràng nhưng không gây stress thị giác.
*   **Tỷ lệ:** 80% giao diện sử dụng màu trung tính – 20% dành cho màu nhấn và cảnh báo.

### 6.1. Nguyên tắc Chung về Màu sắc

*   Không sử dụng màu full saturation cho diện tích lớn.
*   Màu cảnh báo (Alert colors) chỉ nên chiếm tối đa ~20% diện tích màn hình khi hiển thị.
*   Luôn dùng nền nhạt + text/viền đậm cho các thông báo cảnh báo để dễ đọc.
*   Màu sắc cho hành động xóa (Delete action) phải khác biệt rõ ràng với màu sắc trạng thái hết hạn (`Expired`).
*   Chế độ tối (`Dark mode`) không sử dụng nền đen thuần (#000000) để tránh tương phản gắt.

### 6.2. Bảng Màu Chế độ Sáng (Light Mode Palette)

#### 6.2.1. Màu Nền (Neutral Foundation)
| Vai trò        | HEX      | Mục đích                 |
| :------------- | :------- | :----------------------- |
| Background     | `#F4F6F8`  | Nền chính toàn bộ ứng dụng |
| Surface (Card) | `#FFFFFF`  | Nền cho Card, bảng, hộp thoại |
| Border         | `#E0E6ED`  | Viền bảng, input, các thành phần |
| Text Primary   | `#2F3E46`  | Màu chữ nội dung chính    |
| Text Secondary | `#6C7A89`  | Màu chữ cho label phụ, meta info |
*Cảm giác: sạch sẽ, chuyên nghiệp, phù hợp môi trường y tế.*

#### 6.2.2. Màu Hành động Chính (Primary Action)
| Trạng thái     | HEX      |
| :------------- | :------- |
| Primary        | `#2E6F95`  |
| Hover          | `#255D7A`  |
| Active         | `#1F4E66`  |
*Sử dụng cho các nút hành động quan trọng như "Thêm thuốc", các nút chính, hoặc làm nổi bật lựa chọn.*

#### 6.2.3. Hệ thống Cảnh báo (Alert System - Light Mode)
*   **Hết hạn (Danger – Mức độ nghiêm trọng cao)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#C0392B` |
    | Background| `#FDECEA` |
*   **Sắp hết hạn (Warning)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#D68910` |
    | Background| `#FFF4E5` |
*   **Tồn kho thấp (Low Stock)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#B9770E` |
    | Background| `#FEF9E7` |
*   **Thành công (Success)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#1E8449` |
    | Background| `#E8F8F5` |

### 6.3. Bảng Màu Chế độ Tối (Dark Mode Palette)

Chế độ tối được thiết kế dịu mắt, tránh tương phản gắt, không mang phong cách "hacker-style".

#### 6.3.1. Màu Nền (Base Colors - Dark)
| Vai trò        | HEX      | Mục đích                 |
| :------------- | :------- | :----------------------- |
| Background     | `#1F2933`  | Nền chính toàn bộ ứng dụng |
| Surface (Card) | `#273947`  | Nền cho Card, bảng, hộp thoại |
| Border         | `#3E4C59`  | Viền                                 |
| Text Primary   | `#E4E7EB`  | Màu chữ nội dung chính    |
| Text Secondary | `#9AA5B1`  | Màu chữ cho label phụ, meta info |

#### 6.3.2. Màu Hành động Chính (Primary Action - Dark)
| Trạng thái     | HEX      |
| :------------- | :------- |
| Primary        | `#4FA3D1` |
| Hover          | `#3C8DBC` |
| Active         | `#2E6F95` |

#### 6.3.3. Hệ thống Cảnh báo (Alert System - Dark Mode)
*   **Hết hạn (Danger)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#E74C3C` |
    | Background| `#3B1F1C` |
*   **Sắp hết hạn (Warning)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#F1C40F` |
    | Background| `#3D3314` |
*   **Tồn kho thấp (Low Stock)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#E67E22` |
    | Background| `#3B2A16` |
*   **Thành công (Success)**
    | Thành phần | HEX      |
    | :-------- | :------- |
    | Text/Icon | `#2ECC71` |
    | Background| `#1F3D2B` |

### 6.4. Ánh xạ Mức độ Nghiêm trọng -> Màu sắc

| Severity | Trạng thái            | Loại màu        |
| :------- | :-------------------- | :-------------- |
| 3 (Cao)  | Hết hạn / Hết hàng    | Danger (Nguy hiểm) |
| 2        | Sắp hết hạn           | Warning (Cảnh báo) |
| 1        | Tồn kho thấp         | Low Stock (Tồn kho thấp) |

### 6.5. Quy tắc áp dụng trong Bảng Kho (Inventory Table)

*   Không tô màu nền đậm cho toàn bộ hàng. Thay vào đó, sử dụng:
    *   Nền nhạt của màu cảnh báo (Background)
    *   Icon cảnh báo phù hợp.
    *   Màu text đậm (Text/Icon) của màu cảnh báo cho các cột quan trọng (ví dụ: Hạn dùng, Số lượng).
*   Nếu có quá nhiều thuốc cùng lúc bị cảnh báo, chỉ làm nổi bật cột "Hạn dùng" thay vì cả hàng để tránh gây rối mắt.

### 6.6. Trạng thái Vô hiệu hóa (Disabled & States)
| Trạng thái            | Light Mode | Dark Mode |
| :-------------------- | :--------- | :-------- |
| Disabled Background   | `#BDC3C7`  | `#4B5D6B` |
| Disabled Text         | `#95A5A6`  | `#7B8794` |

### 6.7. Tỷ lệ sử dụng màu sắc

Để đảm bảo giao diện cân bằng và không gây rối mắt, tỷ lệ màu sắc khuyến nghị như sau:
*   **80%:** Màu trung tính (xám, trắng, màu nền).
*   **10%:** Màu chính (Primary) – cho các hành động quan trọng.
*   **10%:** Màu cảnh báo (Alert) – cho các thông báo khẩn cấp.
Việc vượt quá tỷ lệ này có thể khiến UI bị "loạn" và mất đi trọng tâm.

### 6.8. Quy tắc khóa cho Beta (Beta Lock Rule)

Trong giai đoạn Beta, các quy tắc sau cần được tuân thủ nghiêm ngặt:
*   Không thay đổi bảng màu (palette) đã định nghĩa.
*   Không thêm màu mới nếu không có vai trò ngữ nghĩa (semantic role) rõ ràng và cần thiết.
*   Tất cả các thay đổi về màu sắc/kiểu dáng phải được kiểm tra độ tương phản trên cả chế độ Sáng và Tối trước khi triển khai.

### 6.9. Hệ thống Typography (Beta Level)

Phần này định nghĩa các quy tắc về kiểu chữ, đảm bảo tính dễ đọc và nhất quán trên toàn ứng dụng.

*   **Nguyên tắc:**
    *   Dễ đọc, phù hợp với môi trường y tế, tránh các kiểu chữ trang trí (`decorative`) hoặc quá "công nghệ" (`tech-style font`).
    *   Nhấn mạnh tính rõ ràng và chức năng.
*   **Lựa chọn Font Family:**
    *   Designer được linh hoạt trong việc lựa chọn font, nhưng font phải là: `Sans-serif` (không chân), `Neutral` (trung tính), `Clean` (sạch sẽ), và không mang phong cách "futuristic" (viễn tưởng).
*   **Thang đo Kích thước & Trọng lượng (Size & Weight Scale) đề xuất:**
    | Vai trò                 | Kích thước (Size) | Trọng lượng (Weight) |
    | :----------------------- | :---------------- | :-------------------- |
    | H1 (Tiêu đề trang)        | 20–22px           | SemiBold              |
    | H2 (Tiêu đề phần)         | 16–18px           | SemiBold              |
    | Body (Nội dung chính)     | 14px              | Regular               |
    | Table text (Văn bản bảng) | 13–14px           | Regular               |
    | Caption / Meta (Phụ chú)  | 12px              | Regular               |
    | Button text (Văn bản nút) | 14px              | Medium                |
*   **Quy tắc quan trọng:**
    *   Không sử dụng quá 5 kích thước (`size`) khác nhau trong toàn bộ ứng dụng.
    *   Không sử dụng 2 font family khác nhau.
    *   Không sử dụng `ALL CAPS` (chữ in hoa toàn bộ) cho các đoạn nội dung dài.
    *   Văn bản cảnh báo (`Alert text`) không được nhỏ hơn kích thước `Body text`.

### 6.10. Quy tắc Khoảng cách và Bố cục (Spacing & Layout Rules)

*   **Đơn vị khoảng cách cơ bản (Spacing base unit):** 8px. Mọi khoảng cách (margin, padding, gap) nên là bội số của 8px để tạo sự hài hòa.
*   **Padding chuẩn:**
    *   `Card padding`: 16px.
    *   `Dialog padding`: 24px.
*   **Border Radius chuẩn:** 8px (để tạo góc bo tròn nhẹ nhàng cho các thành phần như card, button, input).

### 6.11. Hướng dẫn Thành phần (Component Guidelines - Beta Level)

Phần này cung cấp các nguyên tắc cho việc thiết kế các thành phần UI cơ bản.

*   **Nút (Button):**
    *   Sử dụng màu `Primary Action` cho các nút chính.
    *   Các nút phụ hoặc nút hủy có thể dùng màu trung tính hoặc viền.
    *   Chiều cao nút chuẩn, có padding theo `spacing base unit`.
    *   Trạng thái `Hover`, `Active`, `Disabled` cần được thiết kế rõ ràng theo bảng màu đã định nghĩa.
*   **Bảng (Table - `QTableView`):**
    *   Chiều cao hàng chuẩn để đảm bảo dễ đọc.
    *   Phân loại cột: Các cột có thể sắp xếp được cần có chỉ báo sắp xếp rõ ràng.
    *   Mã hóa màu cho trạng thái thuốc (hết hạn, sắp hết hạn, tồn kho thấp) như đã mô tả trong "Trạng thái UI".
*   **Hộp thoại (Dialog - `QDialog`):**
    *   Chiều rộng chuẩn, có thể tùy chỉnh cho từng loại hộp thoại nhưng nên có một vài kích thước tiêu chuẩn (ví dụ: nhỏ, vừa, lớn).
    *   Padding nội dung theo `Dialog padding` (24px).
    *   Các nút hành động (`Save`, `Cancel`) nên được đặt nhất quán (ví dụ: góc dưới bên phải).
*   **Form (Biểu mẫu nhập liệu):**
    *   **Vị trí Label:** Label (nhãn) của trường nhập liệu nên được đặt `trên` (top-aligned) trường input để cải thiện khả năng quét và tiết kiệm không gian ngang.
    *   Các trường nhập liệu (`QLineEdit`, `QComboBox`, `QDateEdit`) cần có kích thước và khoảng cách nhất quán.
    *   Phản hồi xác thực lỗi hiển thị ngay bên dưới trường nhập liệu bị lỗi.

---

## 7. Các Giới hạn Đã biết (Known Limitations) - Phiên bản Beta

Phần này liệt kê các giới hạn của phiên bản Beta, giúp người dùng và đội ngũ phát triển có kỳ vọng đúng đắn và hiểu rõ phạm vi hiện tại của ứng dụng.

*   **Chưa có phân quyền người dùng:** Tất cả người dùng có quyền truy cập đầy đủ vào mọi chức năng.
*   **Dữ liệu lưu trữ cục bộ (Local JSON):** Dữ liệu được lưu trữ trực tiếp trên máy tính cục bộ dưới dạng tệp JSON, không có khả năng đồng bộ đám mây hoặc đa người dùng.
*   **Hiệu suất chưa tối ưu với dữ liệu lớn:** Ứng dụng có thể chưa được tối ưu hoàn toàn khi xử lý số lượng thuốc rất lớn (ví dụ: hơn 10.000 bản ghi).
*   **Chưa có chức năng Hoàn tác (Undo):** Không thể hoàn tác các thao tác như xóa hoặc sửa đổi dữ liệu.
*   **Báo cáo cơ bản:** Chức năng báo cáo còn hạn chế, chưa cung cấp các tùy chọn phân tích nâng cao.

---

## 8. Danh sách Kiểm thử (Testing Checklist) - Phiên bản Beta

Danh sách này cung cấp các điểm kiểm thử cơ bản nhưng quan trọng cho phiên bản Beta, giúp đảm bảo các chức năng cốt lõi hoạt động đúng như mong đợi.

*   **Thêm thuốc:**
    *   Thêm thuốc với tất cả các trường hợp lệ.
    *   Thêm thuốc với ID đã tồn tại (phải báo lỗi).
    *   Thêm thuốc với ID trống (phải tự động tạo ID).
    *   Thêm thuốc với `Số lượng` hoặc `Giá` âm (phải báo lỗi).
    *   Thêm thuốc với `Ngày hết hạn` trong quá khứ (phải báo lỗi hoặc cảnh báo).
    *   Thêm thuốc với `ID Kệ` không tồn tại (phải báo lỗi).
*   **Sửa thuốc:**
    *   Sửa các trường thông tin của thuốc thành công.
    *   Sửa `Số lượng` hoặc `Giá` về giá trị âm (phải báo lỗi).
    *   Sửa `Ngày hết hạn` về giá trị trong quá khứ (phải báo lỗi hoặc cảnh báo).
    *   Sửa `ID Kệ` thành không tồn tại (phải báo lỗi).
*   **Xóa thuốc:**
    *   Xóa thuốc thành công sau khi xác nhận.
    *   Xóa thuốc có `Số lượng > 0` (phải yêu cầu xác nhận mạnh mẽ).
    *   Xóa thuốc đã hết hạn (phải cho phép, có xác nhận).
*   **Tìm kiếm:**
    *   Tìm kiếm chính xác với tên thuốc đầy đủ.
    *   Tìm kiếm mờ (fuzzy search) với tên thuốc sai chính tả hoặc một phần.
    *   Tìm kiếm không ra kết quả (phải hiển thị thông báo "Không tìm thấy").
*   **Bảng điều khiển (Dashboard):**
    *   Hiển thị tóm tắt cảnh báo chính xác.
    *   Kiểm tra biểu đồ (nếu có) có hiển thị đúng dữ liệu.
*   **Cảnh báo:**
    *   Kiểm tra thuốc `hết hạn` được làm nổi bật đúng cách.
    *   Kiểm tra thuốc `sắp hết hạn` được làm nổi bật đúng cách.
    *   Kiểm tra thuốc `tồn kho thấp` được làm nổi bật đúng cách.
    *   Kiểm tra thuốc `hết hàng` được làm nổi bật đúng cách.
*   **Lưu trữ dữ liệu:**
    *   Kiểm tra lưu/tải dữ liệu sau các thao tác CRUD.
    *   Kiểm tra hành vi khi tệp JSON bị hỏng (phải khôi phục từ bản sao lưu hoặc bắt đầu mới).
    *   Kiểm tra hành vi khi không đủ quyền ghi tệp (phải báo lỗi).
*   **Hiệu suất:**
    *   Thử nghiệm với khoảng 1000 bản ghi để đánh giá độ trễ của UI (tính năng có bị lag không).
*   **Chế độ Sáng/Tối:**
    *   Chuyển đổi giữa Light/Dark mode hoạt động chính xác.
    *   Tất cả các thành phần UI hiển thị đúng màu sắc trong cả hai chế độ.
*   **Kiểm thử Khả năng Tiếp cận (Accessibility Check):**
    *   Kiểm tra tỷ lệ tương phản màu sắc (`Contrast ratio`) đạt chuẩn `WCAG AA`.
    *   Màu chữ và màu nền cần đảm bảo độ tương phản đủ cao để dễ đọc. Có thể kiểm tra bằng công cụ online (ví dụ WebAIM Contrast Checker)
    *   Đảm bảo thông tin không chỉ được truyền đạt bằng màu sắc mà còn có các chỉ báo khác (ví dụ: icon, text) để phù hợp với người dùng có khiếm khuyết về thị giác.
    *   Kiểm tra trạng thái focus (`Focus state`) khi điều hướng bằng bàn phím (Tab, Shift+Tab) để đảm bảo tất cả các thành phần tương tác đều có thể truy cập được.
