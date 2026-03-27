"""
Trình quản lý Kho cho Hệ Thống Quản Lý Kho Thuốc.

Module này cung cấp bộ điều khiển trung tâm cho tất cả thao tác kho:
- Thao tác CRUD (Tạo, Đọc, Cập nhật, Xóa) cho thuốc
- Tích hợp với StorageEngine để lưu trữ bền vững
- Kiểm tra và thực thi logic nghiệp vụ
"""
import uuid
from datetime import date
from typing import List, Optional, Dict, Any

from src.models import Medicine, Shelf
from src.storage import StorageEngine


class InventoryManager:
    """
    Bộ điều khiển trung tâm cho thao tác kho.
    
    Quản lý thao tác CRUD cho thuốc với:
    - Tự động sinh ID cho thuốc mới
    - Kiểm tra quy tắc nghiệp vụ
    - Lưu trữ bền vững qua StorageEngine
    - Sắp xếp theo nhiều trường (id, name, quantity, expiry_date, price)
    
    Thuộc tính:
        medicines: Danh sách đối tượng Medicine trong kho
        shelves: Danh sách đối tượng Shelf cho vị trí lưu trữ
        storage: Thực thể StorageEngine cho thao tác file
        medicines_filepath: Đường dẫn tới file JSON thuốc
        shelves_filepath: Đường dẫn tới file JSON kệ
    """
    
    VALID_SORT_FIELDS = ("id", "name", "quantity", "expiry_date", "price")
    
    def __init__(
        self,
        medicines_filepath: str = "data/medicines.json",
        shelves_filepath: str = "data/shelves.json"
    ):
        """
        Khởi tạo InventoryManager.
        
        Tham số:
            medicines_filepath: Đường dẫn tới file JSON thuốc
            shelves_filepath: Đường dẫn tới file JSON kệ
        """
        self.medicines: List[Medicine] = []
        self.shelves: List[Shelf] = []
        self.storage = StorageEngine()
        self.medicines_filepath = medicines_filepath
        self.shelves_filepath = shelves_filepath
    
    def load_data(self) -> None:
        """
        Tải thuốc và kệ từ file JSON.
        
        Xử lý:
        - FileNotFoundError: Khởi tạo danh sách rỗng
        - JSONDecodeError: Ghi log, cố gắng phục hồi từ bản sao lưu
        """
        # Tải thuốc
        try:
            data = self.storage.read_json(self.medicines_filepath)
            self.medicines = [Medicine.from_dict(item) for item in data]
        except FileNotFoundError:
            self.medicines = []
        
        # Tải kệ
        try:
            data = self.storage.read_json(self.shelves_filepath)
            self.shelves = [Shelf.from_dict(item) for item in data]
        except FileNotFoundError:
            self.shelves = []
    
    def save_data(self) -> None:
        """
        Lưu thuốc vào file JSON.
        
        Chuyển đổi tất cả đối tượng Medicine thành dictionary và ghi nguyên tử.
        
        Ngoại lệ:
            IOError: Nếu thao tác ghi thất bại
        """
        data = [medicine.to_dict() for medicine in self.medicines]
        self.storage.write_json(self.medicines_filepath, data)
    
    def save_shelves(self) -> None:
        """
        Lưu kệ vào file JSON.
        
        Ngoại lệ:
            IOError: Nếu thao tác ghi thất bại
        """
        data = [shelf.to_dict() for shelf in self.shelves]
        self.storage.write_json(self.shelves_filepath, data)
    
    def _generate_id(self, shelf_id: str) -> str:
        """
        Tạo ID thuốc duy nhất dựa trên vị trí kệ.
        
        Định dạng: {shelf_id}.{seq:03d}
        Ví dụ: K-A1.001 = Kệ K-A1, Thuốc thứ 001
        
        Tham số:
            shelf_id: ID kệ nơi thuốc sẽ được lưu trữ
            
        Trả về:
            Chuỗi ID duy nhất dựa trên vị trí
        """
        prefix = shelf_id
        
        # Đếm thuốc hiện có cùng tiền tố để xác định số thứ tự
        existing_seq = []
        for med in self.medicines:
            if med.id.startswith(prefix + "."):
                try:
                    seq_part = med.id.split(".")[-1]
                    existing_seq.append(int(seq_part))
                except (ValueError, IndexError):
                    pass
        
        # Số thứ tự tiếp theo
        next_seq = max(existing_seq, default=0) + 1
        
        return f"{prefix}.{next_seq:03d}"

    def _find_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        """
        Tìm thuốc theo ID.
        
        Tham số:
            medicine_id: ID thuốc cần tìm
            
        Trả về:
            Đối tượng Medicine nếu tìm thấy, None nếu không
        """
        for medicine in self.medicines:
            if medicine.id == medicine_id:
                return medicine
        return None
    
    def _find_medicine_index(self, medicine_id: str) -> int:
        """
        Tìm chỉ mục của thuốc theo ID.
        
        Tham số:
            medicine_id: ID thuốc cần tìm
            
        Trả về:
            Chỉ mục thuốc trong danh sách, -1 nếu không tìm thấy
        """
        for i, medicine in enumerate(self.medicines):
            if medicine.id == medicine_id:
                return i
        return -1
        ''' ở dưới có hàm xử lý -> updated
        if index == -1:
            raise ValueError(f"Medicine with ID '{medicine_id}' not found")
        '''
    def _validate_shelf_exists(self, shelf_id: str) -> bool:
        """
        Kiểm tra ID kệ có tồn tại không.
        
        Tham số:
            shelf_id: ID kệ cần kiểm tra
            
        Trả về:
            True nếu kệ tồn tại hoặc chưa tải kệ (cho phép bất kỳ ID)
        """
        # Nếu chưa tải kệ, cho phép bất kỳ shelf_id
        if not self.shelves:
            return True
        
        return any(shelf.id == shelf_id for shelf in self.shelves)
    
    def get_shelf_remaining_capacity(self, shelf_id: str, exclude_medicine_id: str = "") -> int:
        """
        Tính sức chứa còn lại của kệ theo đơn vị số lượng.
        
        Sức chứa = shelf.capacity - tổng(số lượng thuốc trên kệ).
        Nếu cung cấp exclude_medicine_id, số lượng thuốc đó sẽ được loại trừ
        khỏi phép tính đã dùng (hữu ích khi cập nhật thuốc).
        
        Tham số:
            shelf_id: ID kệ
            exclude_medicine_id: ID thuốc để loại trừ khỏi phép tính đã dùng
            
        Trả về:
            Sức chứa còn lại (int). Trả về 0 nếu không tìm thấy kệ.
        """
        shelf = self.get_shelf(shelf_id)
        if not shelf:
            return 0
        
        try:
            total_capacity = int(shelf.capacity)
        except (ValueError, TypeError):
            return 0
        
        used = sum(
            m.quantity for m in self.medicines
            if m.shelf_id == shelf_id and m.id != exclude_medicine_id
        )
        
        return total_capacity - used
    
    def add_medicine(self, medicine: Medicine, auto_save: bool = True) -> Medicine:
        """
        Thêm thuốc mới vào kho.
        
        Tham số:
            medicine: Đối tượng Medicine cần thêm
            auto_save: Nếu True, tự động lưu sau khi thêm
            
        Trả về:
            Đối tượng Medicine đã thêm (có ID được sinh nếu rỗng)
            
        Ngoại lệ:
            ValueError: Nếu ID thuốc đã tồn tại
            ValueError: Nếu shelf_id không hợp lệ
        """
        # Tự sinh ID nếu rỗng
        if not medicine.id:
            new_id = self._generate_id(medicine.shelf_id)
            medicine = Medicine(
                id=new_id,
                name=medicine.name,
                quantity=medicine.quantity,
                expiry_date=medicine.expiry_date,
                shelf_id=medicine.shelf_id,
                price=medicine.price,
                image_path=medicine.image_path
            )
        
        # Kiểm tra ID trùng lặp
        if self._find_medicine_by_id(medicine.id) is not None:
            raise ValueError(f"Thuốc với ID '{medicine.id}' đã tồn tại")
        
        # Kiểm tra kệ tồn tại
        if not self._validate_shelf_exists(medicine.shelf_id):
            raise ValueError(f"Kệ '{medicine.shelf_id}' không tồn tại")
        
        # Kiểm tra sức chứa kệ (chỉ khi đã tải kệ)
        if self.shelves:
            remaining = self.get_shelf_remaining_capacity(medicine.shelf_id)
            if medicine.quantity > remaining:
                raise ValueError(
                    f"Kệ '{medicine.shelf_id}' hiện tại chỉ còn {remaining} "
                    f"đơn vị sức chứa. Vui lòng chọn kệ khác hoặc "
                    f"thay đổi đơn vị thuốc nhập vào"
                )
        
        self.medicines.append(medicine)
        
        if auto_save:
            self.save_data()
        
        return medicine
    
    def remove_medicine(self, medicine_id: str, auto_save: bool = True) -> Medicine:
        """
        Xóa thuốc khỏi kho.
        
        Tham số:
            medicine_id: ID thuốc cần xóa
            auto_save: Nếu True, tự động lưu sau khi xóa
            
        Trả về:
            Đối tượng Medicine đã xóa
            
        Ngoại lệ:
            ValueError: Nếu không tìm thấy thuốc
        """
        index = self._find_medicine_index(medicine_id)
        
        if index == -1:
            raise ValueError(f"Không tìm thấy thuốc với ID '{medicine_id}'")
        
        removed = self.medicines.pop(index)
        
        if auto_save:
            self.save_data()
        
        return removed
    
    def update_medicine(
        self,
        medicine_id: str,
        changes: Dict[str, Any],
        auto_save: bool = True
    ) -> Medicine:
        """
        Cập nhật thuốc với giá trị mới (mẫu bất biến).
        
        Tạo đối tượng Medicine mới với giá trị đã cập nhật.
        Nếu shelf_id thay đổi, ID mới được sinh dựa trên kệ mới.
        
        Tham số:
            medicine_id: ID thuốc cần cập nhật
            changes: Dictionary tên trường tới giá trị mới
            auto_save: Nếu True, tự động lưu sau khi cập nhật
            
        Trả về:
            Đối tượng Medicine đã cập nhật (với ID mới nếu đổi kệ)
            
        Ngoại lệ:
            ValueError: Nếu không tìm thấy thuốc
            ValueError: Nếu thay đổi chứa giá trị không hợp lệ
        """
        index = self._find_medicine_index(medicine_id)
        
        if index == -1:
            raise ValueError(f"Không tìm thấy thuốc với ID '{medicine_id}'")
        
        old_medicine = self.medicines[index]
        
        # Xác định shelf_id mới
        new_shelf_id = changes.get("shelf_id", old_medicine.shelf_id)
        
        # Kiểm tra kệ mới nếu thay đổi
        if "shelf_id" in changes:
            if not self._validate_shelf_exists(new_shelf_id):
                raise ValueError(f"Kệ '{new_shelf_id}' không tồn tại")
        
        # Nếu đổi kệ, sinh ID mới dựa trên kệ mới
        shelf_changed = (
            "shelf_id" in changes
            and changes["shelf_id"] != old_medicine.shelf_id
        )
        if shelf_changed:
            new_id = self._generate_id(new_shelf_id)
        else:
            new_id = old_medicine.id
        
        # Tạo thuốc mới với giá trị đã cập nhật (mẫu bất biến)
        new_medicine = Medicine(
            id=new_id,
            name=changes.get("name", old_medicine.name),
            quantity=changes.get("quantity", old_medicine.quantity),
            expiry_date=changes.get("expiry_date", old_medicine.expiry_date),
            shelf_id=new_shelf_id,
            price=changes.get("price", old_medicine.price),
            image_path=changes.get("image_path", old_medicine.image_path)
        )
        
        # Kiểm tra sức chứa kệ (chỉ khi đã tải kệ và số lượng/kệ thay đổi)
        if self.shelves and ("quantity" in changes or "shelf_id" in changes):
            remaining = self.get_shelf_remaining_capacity(
                new_medicine.shelf_id,
                exclude_medicine_id=old_medicine.id
            )
            if new_medicine.quantity > remaining:
                raise ValueError(
                    f"Kệ '{new_medicine.shelf_id}' hiện tại chỉ còn {remaining} "
                    f"đơn vị sức chứa. Vui lòng chọn kệ khác hoặc "
                    f"thay đổi đơn vị thuốc nhập vào"
                )
        
        # Thay thế trong danh sách
        self.medicines[index] = new_medicine
        
        if auto_save:
            self.save_data()
        
        return new_medicine
    
    def get_medicine(self, medicine_id: str) -> Optional[Medicine]:
        """
        Lấy thuốc theo ID.
        
        Tham số:
            medicine_id: ID thuốc cần lấy
            
        Trả về:
            Đối tượng Medicine nếu tìm thấy, None nếu không
        """
        return self._find_medicine_by_id(medicine_id)
    
    def sort_medicines(
        self,
        sort_by: str = "id",
        ascending: bool = True
    ) -> List[Medicine]:
        """
        Sắp xếp thuốc theo trường chỉ định.
        
        Trả về bản sao đã sắp xếp của danh sách thuốc mà không thay đổi
        thứ tự gốc.
        
        Tham số:
            sort_by: Trường để sắp xếp. Phải là một trong VALID_SORT_FIELDS:
                     'id', 'name', 'quantity', 'expiry_date', 'price'
            ascending: Nếu True, sắp xếp tăng dần; nếu False, giảm dần
            
        Trả về:
            Danh sách mới đã sắp xếp các đối tượng Medicine
            
        Ngoại lệ:
            ValueError: Nếu sort_by không phải tên trường hợp lệ
        """
        if sort_by not in self.VALID_SORT_FIELDS:
            raise ValueError(
                f"Trường sắp xếp không hợp lệ '{sort_by}'. "
                f"Phải là một trong: {', '.join(self.VALID_SORT_FIELDS)}"
            )
        
        # Hàm khóa cho mỗi trường có thể sắp xếp
        key_functions = {
            "id": lambda m: m.id,
            "name": lambda m: m.name.lower(),
            "quantity": lambda m: m.quantity,
            "expiry_date": lambda m: m.expiry_date,
            "price": lambda m: m.price,
        }
        
        return sorted(
            self.medicines,
            key=key_functions[sort_by],
            reverse=not ascending
        )
    
    def get_all_medicines(self) -> List[Medicine]:
        """
        Lấy tất cả thuốc trong kho.
        
        Trả về:
            Danh sách tất cả đối tượng Medicine (bản sao để tránh sửa đổi)
        """
        return list(self.medicines)
    
    def add_shelf(self, shelf: Shelf, auto_save: bool = True) -> Shelf:
        """
        Thêm kệ mới vào lưu trữ.
        
        Tham số:
            shelf: Đối tượng Shelf cần thêm
            auto_save: Nếu True, tự động lưu sau khi thêm
            
        Trả về:
            Đối tượng Shelf đã thêm
            
        Ngoại lệ:
            ValueError: Nếu ID kệ đã tồn tại
        """
        # Kiểm tra ID trùng lặp
        if any(s.id == shelf.id for s in self.shelves):
            raise ValueError(f"Kệ với ID '{shelf.id}' đã tồn tại")
        
        self.shelves.append(shelf)
        
        if auto_save:
            self.save_shelves()
        
        return shelf
    
    def get_shelf(self, shelf_id: str) -> Optional[Shelf]:
        """
        Lấy kệ theo ID.
        
        Tham số:
            shelf_id: ID kệ cần lấy
            
        Trả về:
            Đối tượng Shelf nếu tìm thấy, None nếu không
        """
        for shelf in self.shelves:
            if shelf.id == shelf_id:
                return shelf
        return None
    
    def update_shelf(
        self,
        shelf_id: str,
        changes: Dict[str, Any],
        auto_save: bool = True
    ) -> Shelf:
        """
        Cập nhật kệ với giá trị mới (mẫu bất biến).
        
        Tham số:
            shelf_id: ID kệ cần cập nhật
            changes: Dictionary tên trường tới giá trị mới
            auto_save: Nếu True, tự động lưu sau khi cập nhật
            
        Trả về:
            Đối tượng Shelf đã cập nhật
            
        Ngoại lệ:
            ValueError: Nếu không tìm thấy kệ
        """
        index = -1
        for i, shelf in enumerate(self.shelves):
            if shelf.id == shelf_id:
                index = i
                break
        
        if index == -1:
            raise ValueError(f"Không tìm thấy kệ với ID '{shelf_id}'")
        
        old_shelf = self.shelves[index]
        
        new_shelf = Shelf(
            id=old_shelf.id,
            zone=changes.get("zone", old_shelf.zone),
            row=changes.get("row", old_shelf.row),
            column=changes.get("column", old_shelf.column),
            capacity=changes.get("capacity", old_shelf.capacity)
        )
        
        self.shelves[index] = new_shelf
        
        if auto_save:
            self.save_shelves()
        
        return new_shelf
    
    def remove_shelf(self, shelf_id: str, auto_save: bool = True) -> Shelf:
        """
        Xóa kệ khỏi lưu trữ.
        
        Tham số:
            shelf_id: ID kệ cần xóa
            auto_save: Nếu True, tự động lưu sau khi xóa
            
        Trả về:
            Đối tượng Shelf đã xóa
            
        Ngoại lệ:
            ValueError: Nếu không tìm thấy kệ hoặc vẫn còn thuốc
        """
        medicines_on_shelf = [
            m for m in self.medicines if m.shelf_id == shelf_id
        ]
        if medicines_on_shelf:
            raise ValueError(
                f"Không thể xóa kệ '{shelf_id}': "
                f"vẫn còn {len(medicines_on_shelf)} thuốc trên kệ này"
            )
        
        index = -1
        for i, shelf in enumerate(self.shelves):
            if shelf.id == shelf_id:
                index = i
                break
        
        if index == -1:
            raise ValueError(f"Không tìm thấy kệ với ID '{shelf_id}'")
        
        removed = self.shelves.pop(index)
        
        if auto_save:
            self.save_shelves()
        
        return removed
    
    def get_all_shelves(self) -> List[Shelf]:
        """
        Lấy tất cả kệ.
        
        Trả về:
            Danh sách tất cả đối tượng Shelf (bản sao để tránh sửa đổi)
          """
        return list(self.shelves)
