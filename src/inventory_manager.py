"""
Inventory Manager for Pharmacy Management System.

This module provides the central controller for all inventory operations:
- CRUD operations (Create, Read, Update, Delete) for medicines
- Integration with StorageEngine for persistence
- Validation and business logic enforcement
"""
import uuid
from datetime import date
from typing import List, Optional, Dict, Any

from src.models import Medicine, Shelf
from src.storage import StorageEngine


class InventoryManager:
    """
    Central controller for inventory operations.
    
    Manages CRUD operations for medicines with:
    - Automatic ID generation for new medicines
    - Validation of business rules
    - Persistence via StorageEngine
    - Sorting by various fields (id, name, quantity, expiry_date, price)
    
    Attributes:
        medicines: List of Medicine objects in inventory
        shelves: List of Shelf objects for storage locations
        storage: StorageEngine instance for file operations
        medicines_filepath: Path to medicines JSON file
        shelves_filepath: Path to shelves JSON file
    """
    
    VALID_SORT_FIELDS = ("id", "name", "quantity", "expiry_date", "price")
    
    def __init__(
        self,
        medicines_filepath: str = "data/medicines.json",
        shelves_filepath: str = "data/shelves.json"
    ):
        """
        Initialize InventoryManager.
        
        Args:
            medicines_filepath: Path to medicines JSON file
            shelves_filepath: Path to shelves JSON file
        """
        self.medicines: List[Medicine] = []
        self.shelves: List[Shelf] = []
        self.storage = StorageEngine()
        self.medicines_filepath = medicines_filepath
        self.shelves_filepath = shelves_filepath
    
    def load_data(self) -> None:
        """
        Load medicines and shelves from JSON files.
        
        Handles:
        - FileNotFoundError: Initializes empty list
        - JSONDecodeError: Logged, attempts backup recovery
        """
        # Load medicines
        try:
            data = self.storage.read_json(self.medicines_filepath)
            self.medicines = [Medicine.from_dict(item) for item in data]
        except FileNotFoundError:
            self.medicines = []
        
        # Load shelves
        try:
            data = self.storage.read_json(self.shelves_filepath)
            self.shelves = [Shelf.from_dict(item) for item in data]
        except FileNotFoundError:
            self.shelves = []
    
    def save_data(self) -> None:
        """
        Persist medicines to JSON file.
        
        Converts all Medicine objects to dictionaries and writes atomically.
        
        Raises:
            IOError: If write operation fails
        """
        data = [medicine.to_dict() for medicine in self.medicines]
        self.storage.write_json(self.medicines_filepath, data)
    
    def save_shelves(self) -> None:
        """
        Persist shelves to JSON file.
        
        Raises:
            IOError: If write operation fails
        """
        data = [shelf.to_dict() for shelf in self.shelves]
        self.storage.write_json(self.shelves_filepath, data)
    
    def _generate_id(self, shelf_id: str) -> str:
        """
        Generate a unique medicine ID based on shelf location.
        
        Format: {shelf_id}.{seq:03d}
        Example: K-A1.001 = Kệ K-A1, Thuốc thứ 001
        
        Args:
            shelf_id: ID of the shelf where the medicine will be stored
            
        Returns:
            Unique location-based ID string
        """
        prefix = shelf_id
        
        # Count existing medicines with the same prefix to determine sequence
        existing_seq = []
        for med in self.medicines:
            if med.id.startswith(prefix + "."):
                try:
                    seq_part = med.id.split(".")[-1]
                    existing_seq.append(int(seq_part))
                except (ValueError, IndexError):
                    pass
        
        # Next sequence number
        next_seq = max(existing_seq, default=0) + 1
        
        return f"{prefix}.{next_seq:03d}"

    def _find_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        """
        Find medicine by ID.
        
        Args:
            medicine_id: ID of medicine to find
            
        Returns:
            Medicine object if found, None otherwise
        """
        for medicine in self.medicines:
            if medicine.id == medicine_id:
                return medicine
        return None
    
    def _find_medicine_index(self, medicine_id: str) -> int:
        """
        Find index of medicine by ID.
        
        Args:
            medicine_id: ID of medicine to find
            
        Returns:
            Index of medicine in list, -1 if not found
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
        Check if a shelf ID exists.
        
        Args:
            shelf_id: ID of shelf to validate
            
        Returns:
            True if shelf exists or if no shelves loaded (allows any ID)
        """
        # If no shelves loaded, allow any shelf_id
        if not self.shelves:
            return True
        
        return any(shelf.id == shelf_id for shelf in self.shelves)
    
    def get_shelf_remaining_capacity(self, shelf_id: str, exclude_medicine_id: str = "") -> int:
        """
        Calculate remaining capacity of a shelf in quantity units.
        
        Capacity = shelf.capacity - sum(quantity of all medicines on shelf).
        If exclude_medicine_id is provided, that medicine's quantity is excluded
        from the used calculation (useful when updating a medicine).
        
        Args:
            shelf_id: ID of the shelf
            exclude_medicine_id: Medicine ID to exclude from used calculation
            
        Returns:
            Remaining capacity (int). Returns 0 if shelf not found.
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
        Add a new medicine to inventory.
        
        Args:
            medicine: Medicine object to add
            auto_save: If True, automatically save after adding
            
        Returns:
            Added Medicine object (with generated ID if empty)
            
        Raises:
            ValueError: If medicine ID already exists
            ValueError: If shelf_id is invalid
        """
        # Auto-generate ID if empty
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
        
        # Check for duplicate ID
        if self._find_medicine_by_id(medicine.id) is not None:
            raise ValueError(f"Medicine with ID '{medicine.id}' already exists")
        
        # Validate shelf exists
        if not self._validate_shelf_exists(medicine.shelf_id):
            raise ValueError(f"Shelf '{medicine.shelf_id}' does not exist")
        
        # Validate shelf capacity (only if shelves are loaded)
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
        Remove a medicine from inventory.
        
        Args:
            medicine_id: ID of medicine to remove
            auto_save: If True, automatically save after removing
            
        Returns:
            Removed Medicine object
            
        Raises:
            ValueError: If medicine not found
        """
        index = self._find_medicine_index(medicine_id)
        
        if index == -1:
            raise ValueError(f"Medicine with ID '{medicine_id}' not found")
        
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
        Update a medicine with new values (immutable pattern).
        
        Creates a new Medicine object with updated values.
        
        Args:
            medicine_id: ID of medicine to update
            changes: Dictionary of field names to new values
            auto_save: If True, automatically save after updating
            
        Returns:
            Updated Medicine object
            
        Raises:
            ValueError: If medicine not found
            ValueError: If changes contain invalid values
        """
        index = self._find_medicine_index(medicine_id)
        
        if index == -1:
            raise ValueError(f"Medicine with ID '{medicine_id}' not found")
        
        old_medicine = self.medicines[index]
        
        # Create new medicine with updated values (immutable pattern)
        new_medicine = Medicine(
            id=old_medicine.id,  # ID cannot be changed
            name=changes.get("name", old_medicine.name),
            quantity=changes.get("quantity", old_medicine.quantity),
            expiry_date=changes.get("expiry_date", old_medicine.expiry_date),
            shelf_id=changes.get("shelf_id", old_medicine.shelf_id),
            price=changes.get("price", old_medicine.price),
            image_path=changes.get("image_path", old_medicine.image_path)
        )
        
        # Validate new shelf if changed
        if "shelf_id" in changes:
            if not self._validate_shelf_exists(new_medicine.shelf_id):
                raise ValueError(f"Shelf '{new_medicine.shelf_id}' does not exist")
        
        # Validate shelf capacity (only if shelves are loaded and quantity/shelf changed)
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
        
        # Replace in list
        self.medicines[index] = new_medicine
        
        if auto_save:
            self.save_data()
        
        return new_medicine
    
    def get_medicine(self, medicine_id: str) -> Optional[Medicine]:
        """
        Get a medicine by ID.
        
        Args:
            medicine_id: ID of medicine to retrieve
            
        Returns:
            Medicine object if found, None otherwise
        """
        return self._find_medicine_by_id(medicine_id)
    
    def sort_medicines(
        self,
        sort_by: str = "id",
        ascending: bool = True
    ) -> List[Medicine]:
        """
        Sort medicines by a specified field.
        
        Returns a sorted copy of the medicines list without modifying
        the original order.
        
        Args:
            sort_by: Field to sort by. Must be one of VALID_SORT_FIELDS:
                     'id', 'name', 'quantity', 'expiry_date', 'price'
            ascending: If True, sort ascending; if False, sort descending
            
        Returns:
            New sorted list of Medicine objects
            
        Raises:
            ValueError: If sort_by is not a valid field name
        """
        if sort_by not in self.VALID_SORT_FIELDS:
            raise ValueError(
                f"Invalid sort field '{sort_by}'. "
                f"Must be one of: {', '.join(self.VALID_SORT_FIELDS)}"
            )
        
        # Key functions for each sortable field
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
        Get all medicines in inventory.
        
        Returns:
            List of all Medicine objects (copy to prevent modification)
        """
        return list(self.medicines)
    
    def add_shelf(self, shelf: Shelf, auto_save: bool = True) -> Shelf:
        """
        Add a new shelf to storage.
        
        Args:
            shelf: Shelf object to add
            auto_save: If True, automatically save after adding
            
        Returns:
            Added Shelf object
            
        Raises:
            ValueError: If shelf ID already exists
        """
        # Check for duplicate ID
        if any(s.id == shelf.id for s in self.shelves):
            raise ValueError(f"Shelf with ID '{shelf.id}' already exists")
        
        self.shelves.append(shelf)
        
        if auto_save:
            self.save_shelves()
        
        return shelf
    
    def get_shelf(self, shelf_id: str) -> Optional[Shelf]:
        """
        Get a shelf by ID.
        
        Args:
            shelf_id: ID of shelf to retrieve
            
        Returns:
            Shelf object if found, None otherwise
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
        Update a shelf with new values (immutable pattern).
        
        Args:
            shelf_id: ID of shelf to update
            changes: Dictionary of field names to new values
            auto_save: If True, automatically save after updating
            
        Returns:
            Updated Shelf object
            
        Raises:
            ValueError: If shelf not found
        """
        index = -1
        for i, shelf in enumerate(self.shelves):
            if shelf.id == shelf_id:
                index = i
                break
        
        if index == -1:
            raise ValueError(f"Shelf with ID '{shelf_id}' not found")
        
        old_shelf = self.shelves[index]
        
        new_shelf = Shelf(
            id=old_shelf.id,
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
        Remove a shelf from storage.
        
        Args:
            shelf_id: ID of shelf to remove
            auto_save: If True, automatically save after removing
            
        Returns:
            Removed Shelf object
            
        Raises:
            ValueError: If shelf not found or still has medicines
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
            raise ValueError(f"Shelf with ID '{shelf_id}' not found")
        
        removed = self.shelves.pop(index)
        
        if auto_save:
            self.save_shelves()
        
        return removed
    
    def get_all_shelves(self) -> List[Shelf]:
        """
        Get all shelves.
        
        Returns:
            List of all Shelf objects (copy to prevent modification)
        """
        return list(self.shelves)
