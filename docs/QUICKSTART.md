# 🚀 Hướng Dẫn Nhanh - Hệ Thống Quản Lý Kho Thuốc

## Cài Đặt Nhanh

### Bước 1: Cài Python

- Tải Python 3.13 từ: <https://www.python.org/downloads/>
- Chọn **"Add Python to PATH"** khi cài đặt

### Bước 2: Cài Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy Ứng Dụng

**Cách 1 - Sử dụng script:**

```
run.bat
```

**Cách 2 - Command line:**

```bash
python app.py
```

## Sử Dụng Cơ Bản

### ➕ Thêm Thuốc

1. Nhấn **"➕ Thêm thuốc mới"** hoặc `Ctrl+N`
2. Điền thông tin:
   - Tên thuốc (bắt buộc)
   - Số lượng
   - Hạn sử dụng
   - Giá
   - Kệ
3. Nhấn **"Thêm thuốc"**

### ✏️ Sửa Thuốc

- Double-click vào thuốc trong bảng
- HOẶC: Chuột phải → **"✏️ Sửa thuốc"**

### 🗑️ Xóa Thuốc

- Chuột phải → **"🗑️ Xóa thuốc"**
- Xác nhận xóa

### 🔍 Tìm Kiếm

1. Nhấn `Ctrl+K` hoặc **"🔍 Tìm kiếm"**
2. Nhập tên thuốc
3. Chọn kết quả

### 📊 Xem Dashboard

- Click **"📊 Bảng điều khiển"** trên sidebar
- Xem thống kê và biểu đồ

### 🌙 Đổi Theme

- Nhấn `Ctrl+D`
- HOẶC: Click **"🌙 Chế độ tối"**

## Phím Tắt

| Phím Tắt | Chức Năng |
|----------|-----------|
| `Ctrl+K` | Tìm kiếm nhanh |
| `Ctrl+N` | Thêm thuốc |
| `Ctrl+D` | Đổi Light/Dark mode |

## Hiểu Trạng Thái Thuốc

### ❌ Hết Hạn (Đỏ)

- Thuốc đã quá hạn sử dụng
- **Hành động:** Kiểm tra và loại bỏ

### ⏰ Sắp Hết Hạn (Vàng)

- Còn dưới 30 ngày đến hạn
- **Hành động:** Ưu tiên sử dụng hoặc khuyến mãi

### 📉 Tồn Kho Thấp (Cam)

- Số lượng ≤ 5 đơn vị
- **Hành động:** Đặt hàng bổ sung

### 🚫 Hết Hàng (Đỏ)

- Số lượng = 0
- **Hành động:** Nhập hàng ngay

### ✅ Bình Thường (Không màu)

- Thuốc còn hạn và đủ tồn kho

## Xử Lý Lỗi

### Không tìm thấy dữ liệu

- Ứng dụng tự động tạo file `medicines.json` và `shelves.json`
- Thêm thuốc và kệ mới để bắt đầu

### Dữ liệu bị hỏng

- Hệ thống tự động khôi phục từ `.backup`
- Kiểm tra thư mục `data/`

### Lỗi khi lưu

- Kiểm tra quyền ghi file
- Đảm bảo đủ dung lượng ổ đĩa

## Tips & Tricks

### 💡 Quản lý kệ hiệu quả

- Đặt tên kệ theo vị trí thực tế (A1, B2, C3...)
- Nhóm thuốc cùng loại vào cùng kệ

### 💡 Tránh hết hạn

- Kiểm tra Dashboard thường xuyên
- Chú ý cảnh báo màu vàng (sắp hết hạn)
- Áp dụng nguyên tắc FIFO (First In First Out)

### 💡 Tìm kiếm nhanh

- Dùng `Ctrl+K` thay vì cuộn bảng
- Tìm kiếm mờ hỗ trợ cả lỗi chính tả

### 💡 Nhập liệu nhanh

- Dùng `Tab` để chuyển giữa các trường
- Hạn dùng mặc định: +1 năm từ hôm nay
- ID tự động tạo khi để trống

## Sao lưu dữ liệu

### Tự động

- File backup tạo mỗi khi lưu: `medicines.json.backup`

### Thủ công

- Copy thư mục `data/` ra nơi khác
- Lưu vào USB hoặc cloud

## Khôi phục dữ liệu

1. Đóng ứng dụng
2. Đổi tên `medicines.json.backup` → `medicines.json`
3. Khởi động lại ứng dụng

## Liên Hệ Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra README.md
2. Xem file log (nếu có)
3. Báo lỗi qua Issues trên GitHub

---

**Chúc bạn sử dụng hiệu quả!** 🎉
