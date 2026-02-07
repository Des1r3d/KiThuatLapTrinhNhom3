"""
Data models for Pharmacy Management System.

This module contains the core data classes:
- Medicine: Represents a medicine item in inventory
- Shelf: Represents a physical storage location
"""
from dataclasses import dataclass
from datetime import date
from typing import Dict, Any


@dataclass
class Medicine:
    """
    Represents a medicine item in the pharmacy inventory.

    Attributes:
        id: Unique identifier (auto-generated if empty)
        name: Medicine name
        quantity: Stock quantity (must be >= 0)
        expiry_date: Expiration date
        shelf_id: Reference to storage location
        price: Unit price (must be >= 0)
    """
    id: str
    name: str
    quantity: int
    expiry_date: date
    shelf_id: str
    price: float

    def __post_init__(self):
        """Validate medicine data after initialization."""
        if self.quantity < 0:
            raise ValueError("Quantity must be >= 0")
        if self.price < 0:
            raise ValueError("Price must be >= 0")

    def is_expired(self) -> bool:
        """
        Check if medicine is expired.

        Returns:
            True if expiry_date <= today, False otherwise
        """
        return self.expiry_date <= date.today()

    def days_until_expiry(self) -> int:
        """
        Calculate days until expiry.

        Returns:
            Number of days until expiry (negative if already expired)
        """
        delta = self.expiry_date - date.today()
        return delta.days

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Medicine to dictionary for JSON storage.

        Returns:
            Dictionary with all attributes, date converted to ISO string
        """
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date.isoformat(),
            "shelf_id": self.shelf_id,
            "price": self.price
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Medicine':
        """
        Deserialize Medicine from dictionary.

        Args:
            data: Dictionary containing medicine data

        Returns:
            Medicine object

        Raises:
            KeyError: If required field is missing
            ValueError: If date format is invalid or validation fails
        """
        return Medicine(
            id=data["id"],
            name=data["name"],
            quantity=data["quantity"],
            expiry_date=date.fromisoformat(data["expiry_date"]),
            shelf_id=data["shelf_id"],
            price=data["price"]
        )


@dataclass
class Shelf:
    """
    Represents a physical storage location in the pharmacy.

    Attributes:
        id: Shelf identifier
        row: Row position
        column: Column position
        capacity: Maximum capacity
    """
    id: str
    row: str
    column: str
    capacity: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Shelf to dictionary for JSON storage.

        Returns:
            Dictionary with all attributes
        """
        return {
            "id": self.id,
            "row": self.row,
            "column": self.column,
            "capacity": self.capacity
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Shelf':
        """
        Deserialize Shelf from dictionary.

        Args:
            data: Dictionary containing shelf data

        Returns:
            Shelf object

        Raises:
            KeyError: If required field is missing
        """
        return Shelf(
            id=data["id"],
            row=data["row"],
            column=data["column"],
            capacity=data["capacity"]
        )
