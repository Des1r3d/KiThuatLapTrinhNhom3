"""
Model dữ liệu cho Hệ Thống Quản Lý Kho Thuốc.

Module này chứa các lớp dữ liệu chính:
- Medicine: Đại diện một mục thuốc trong kho
- Shelf: Đại diện một vị trí lưu trữ vật lý
"""
from dataclasses import dataclass
from datetime import date
from typing import Dict, Any


@dataclass
class Medicine:
    """
    Đại diện một mục thuốc trong kho dược phẩm.

    Thuộc tính:
        id: Mã định danh duy nhất (tự sinh nếu rỗng)
        name: Tên thuốc
        quantity: Số lượng tồn kho (phải >= 0)
        expiry_date: Ngày hết hạn
        shelf_id: Tham chiếu tới vị trí lưu trữ
        price: Đơn giá (phải >= 0)
        image_path: Đường dẫn tùy chọn tới ảnh thuốc (tương đối với data/images/)
    """
    id: str
    name: str
    quantity: int
    expiry_date: date
    shelf_id: str
    price: float
    image_path: str = ""

    def __post_init__(self):
        """Kiểm tra dữ liệu thuốc sau khi khởi tạo."""
        if self.quantity < 0:
            raise ValueError("Số lượng phải >= 0")
        if self.price < 0:
            raise ValueError("Giá phải >= 0")

    def is_expired(self) -> bool:
        """
        Kiểm tra thuốc đã hết hạn chưa.

        Trả về:
            True nếu expiry_date <= hôm nay, False nếu ngược lại
        """
        return self.expiry_date <= date.today()

    def days_until_expiry(self) -> int:
        """
        Tính số ngày còn lại đến hạn sử dụng.

        Trả về:
            Số ngày đến hạn (âm nếu đã hết hạn)
        """
        delta = self.expiry_date - date.today()
        return delta.days

    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi Medicine thành dictionary để lưu JSON.

        Trả về:
            Dictionary với tất cả thuộc tính, ngày chuyển thành chuỗi ISO
        """
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date.isoformat(),
            "shelf_id": self.shelf_id,
            "price": self.price,
            "image_path": self.image_path
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Medicine':
        """
        Giải tuần tự hóa Medicine từ dictionary.

        Tham số:
            data: Dictionary chứa dữ liệu thuốc

        Trả về:
            Đối tượng Medicine

        Ngoại lệ:
            KeyError: Nếu thiếu trường bắt buộc
            ValueError: Nếu định dạng ngày không hợp lệ hoặc kiểm tra thất bại
        """
        return Medicine(
            id=data["id"],
            name=data["name"],
            quantity=data["quantity"],
            expiry_date=date.fromisoformat(data["expiry_date"]),
            shelf_id=data["shelf_id"],
            price=data["price"],
            image_path=data.get("image_path", "")
        )


@dataclass
class Shelf:
    """
    Đại diện vị trí lưu trữ vật lý trong nhà thuốc.

    Thuộc tính:
        id: Mã kệ, VD: "K-A1" (định dạng: {khu}-{cột}{dãy})
        zone: Mã khu/vùng (Khu), VD: "K"
        column: Chữ cái cột (Cột), VD: "A", "B"
        row: Số dãy (Dãy), VD: "1", "2"
        capacity: Sức chứa tối đa
    """
    id: str
    zone: str
    column: str
    row: str
    capacity: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi Shelf thành dictionary để lưu JSON.

        Trả về:
            Dictionary với tất cả thuộc tính
        """
        return {
            "id": self.id,
            "zone": self.zone,
            "column": self.column,
            "row": self.row,
            "capacity": self.capacity
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Shelf':
        """
        Giải tuần tự hóa Shelf từ dictionary.

        Tham số:
            data: Dictionary chứa dữ liệu kệ

        Trả về:
            Đối tượng Shelf

        Ngoại lệ:
            KeyError: Nếu thiếu trường bắt buộc
        """
        return Shelf(
            id=data["id"],
            zone=data["zone"],
            column=data["column"],
            row=data["row"],
            capacity=data["capacity"]
        )
