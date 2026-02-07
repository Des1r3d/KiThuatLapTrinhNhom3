# Báo Cáo Tiến Độ - Hệ Thống Quản Lý Kho Thuốc

**Cập nhật lần cuối:** 07-02-2026

## Trạng Thái Dự Án: Giai Đoạn 1 Hoàn Thành ✓

### Tóm Tắt

Tầng nền tảng của Hệ Thống Quản Lý Kho Thuốc đã được triển khai thành công. Bao gồm các lớp dữ liệu cốt lõi và engine lưu trữ, cả hai đều có độ phủ test toàn diện.

---

## Các Ticket Đã Hoàn Thành

### T-102: Mô Hình Dữ Liệu ✓

**Tệp tin:**
- `src/models.py` - Các lớp dữ liệu cốt lõi

**Chi tiết triển khai:**

1. **Lớp Medicine** (dataclass)
   - Đầy đủ thuộc tính: id, name, quantity, expiry_date, shelf_id, price
   - Validation trong `__post_init__`: quantity >= 0, price >= 0
   - `is_expired()` - Trả về True nếu thuốc đã hết hạn
   - `days_until_expiry()` - Trả về số ngày còn lại đến hạn (âm nếu đã hết hạn)
   - `to_dict()` - Chuyển đổi sang JSON với định dạng ngày ISO
   - `from_dict()` - Phương thức tĩnh để khôi phục từ JSON

2. **Lớp Shelf** (dataclass)
   - Đầy đủ thuộc tính: id, row, column, capacity
   - `to_dict()` - Chuyển đổi sang JSON
   - `from_dict()` - Phương thức tĩnh để khôi phục từ JSON

**Độ phủ test:** 17 test trong `tests/test_models.py`
- Test validation (số lượng âm, giá âm)
- Test logic hết hạn (đã hết hạn, chưa hết hạn, hết hạn hôm nay)
- Test chuyển đổi dữ liệu hai chiều (serialization/deserialization)
- Test xử lý lỗi (thiếu trường, định dạng ngày không hợp lệ)

---

### T-103: Engine Lưu Trữ ✓

**Tệp tin:**
- `src/storage.py` - Các thao tác với tệp JSON

**Chi tiết triển khai:**

1. **Lớp StorageEngine**
   - `write_json(filepath, data)` - Ghi atomic
     - Tự động tạo thư mục cha nếu chưa tồn tại
     - Tạo bản sao lưu trước khi ghi
     - Ghi vào tệp tạm (.tmp) trước
     - Đổi tên atomic sang tên tệp cuối cùng
     - Khôi phục từ bản sao lưu nếu thất bại
   - `read_json(filepath)` - Đọc an toàn
     - Kiểm tra tệp tồn tại
     - Xử lý JSON bị hỏng bằng cách khôi phục từ bản sao lưu
     - Hỗ trợ đầy đủ UTF-8 (tiếng Việt, tiếng Trung, emoji)

**Độ phủ test:** 12 test trong `tests/test_storage.py`
- Thao tác đọc/ghi cơ bản
- Xác minh ghi atomic
- Tạo và khôi phục bản sao lưu
- Xử lý ký tự Unicode
- Tạo thư mục tự động
- Xử lý lỗi (không tìm thấy tệp, JSON không hợp lệ)

---

## Kết Quả Test

```
============================= test session starts =============================
platform win32 -- Python 3.13.7
collected 29 items

tests/test_models.py::TestMedicine (13 tests)              PASSED
tests/test_models.py::TestShelf (4 tests)                  PASSED
tests/test_storage.py::TestStorageEngine (12 tests)        PASSED

============================= 29 passed in 0.16s ==============================
```

---

## Công Việc Còn Lại

### Giai Đoạn 2: Logic Nghiệp Vụ

| Ticket | Thành Phần | Trạng Thái |
|--------|------------|------------|
| T-201 | Quản Lý Kho (Inventory Manager) | Chưa bắt đầu |
| T-202 | Hệ Thống Cảnh Báo (Alert System) | Chưa bắt đầu |
| T-203 | Công Cụ Tìm Kiếm (Search Engine) | Chưa bắt đầu |

### Giai Đoạn 3: Giao Diện Người Dùng

| Ticket | Thành Phần | Trạng Thái |
|--------|------------|------------|
| T-301 | Cửa Sổ Chính (Main Window) | Chưa bắt đầu |
| T-302 | Giao Diện Kho (Inventory View) | Chưa bắt đầu |
| T-303 | Hộp Thoại Thêm/Sửa (Add/Edit Dialog) | Chưa bắt đầu |
| T-304 | Bảng Điều Khiển (Dashboard) | Chưa bắt đầu |
| T-305 | Chuyển Đổi Giao Diện (Theme Toggle) | Chưa bắt đầu |

---

## Ghi Chú Kiến Trúc

Triển khai hiện tại tuân theo:
- **Repository Pattern**: StorageEngine trừu tượng hóa thao tác tệp
- **Immutable Patterns**: Medicine/Shelf là dataclass bất biến
- **Atomic Operations**: Ghi sử dụng chiến lược tệp tạm + đổi tên
- **Error Recovery**: Cơ chế sao lưu để đảm bảo an toàn dữ liệu

---

## Bước Tiếp Theo

1. Triển khai `InventoryManager` (T-201) cho các thao tác CRUD
2. Thêm `AlertSystem` (T-202) để phát hiện thuốc sắp hết hạn/tồn kho thấp
3. Triển khai `SearchEngine` (T-203) với tìm kiếm mờ TheFuzz
