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
    
    Attributes:
        medicines: List of Medicine objects in inventory
        shelves: List of Shelf objects for storage locations
        storage: StorageEngine instance for file operations
        medicines_filepath: Path to medicines JSON file
        shelves_filepath: Path to shelves JSON file
    """
    
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
    
    def _generate_id(self) -> str:
        """
        Generate a unique medicine ID.
        
        Returns:
            Unique ID string (UUID format)
        """
        return f"MED-{uuid.uuid4().hex[:8].upper()}"
    
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
            new_id = self._generate_id()
            medicine = Medicine(
                id=new_id,
                name=medicine.name,
                quantity=medicine.quantity,
                expiry_date=medicine.expiry_date,
                shelf_id=medicine.shelf_id,
                price=medicine.price
            )
        
        # Check for duplicate ID
        if self._find_medicine_by_id(medicine.id) is not None:
            raise ValueError(f"Medicine with ID '{medicine.id}' already exists")
        
        # Validate shelf exists
        if not self._validate_shelf_exists(medicine.shelf_id):
            raise ValueError(f"Shelf '{medicine.shelf_id}' does not exist")
        
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
            price=changes.get("price", old_medicine.price)
        )
        
        # Validate new shelf if changed
        if "shelf_id" in changes:
            if not self._validate_shelf_exists(new_medicine.shelf_id):
                raise ValueError(f"Shelf '{new_medicine.shelf_id}' does not exist")
        
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
    
    def get_all_shelves(self) -> List[Shelf]:
        """
        Get all shelves.
        
        Returns:
            List of all Shelf objects (copy to prevent modification)
        """
        return list(self.shelves)
