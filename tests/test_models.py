"""
Test suite for Medicine and Shelf data models.
Tests cover validation, serialization, and business logic.
"""
import pytest
from datetime import date, timedelta
from src.models import Medicine, Shelf


class TestMedicine:
    """Test suite for Medicine class."""

    def test_medicine_creation_valid(self):
        """Test creating a valid Medicine object."""
        medicine = Medicine(
            id="MED001",
            name="Paracetamol 500mg",
            quantity=100,
            expiry_date=date(2025, 12, 31),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.id == "MED001"
        assert medicine.name == "Paracetamol 500mg"
        assert medicine.quantity == 100
        assert medicine.expiry_date == date(2025, 12, 31)
        assert medicine.shelf_id == "SHELF-A1"
        assert medicine.price == 5.99

    def test_medicine_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be >= 0"):
            Medicine(
                id="MED001",
                name="Paracetamol",
                quantity=-5,
                expiry_date=date(2025, 12, 31),
                shelf_id="SHELF-A1",
                price=5.99
            )

    def test_medicine_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be >= 0"):
            Medicine(
                id="MED001",
                name="Paracetamol",
                quantity=10,
                expiry_date=date(2025, 12, 31),
                shelf_id="SHELF-A1",
                price=-5.99
            )

    def test_is_expired_returns_true_for_past_date(self):
        """Test is_expired returns True for expired medicine."""
        medicine = Medicine(
            id="MED001",
            name="Expired Medicine",
            quantity=10,
            expiry_date=date.today() - timedelta(days=1),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.is_expired() is True

    def test_is_expired_returns_false_for_future_date(self):
        """Test is_expired returns False for valid medicine."""
        medicine = Medicine(
            id="MED001",
            name="Valid Medicine",
            quantity=10,
            expiry_date=date.today() + timedelta(days=30),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.is_expired() is False

    def test_is_expired_returns_true_for_today(self):
        """Test is_expired returns True for medicine expiring today."""
        medicine = Medicine(
            id="MED001",
            name="Expiring Today",
            quantity=10,
            expiry_date=date.today(),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.is_expired() is True

    def test_days_until_expiry_positive(self):
        """Test days_until_expiry returns positive for future date."""
        medicine = Medicine(
            id="MED001",
            name="Valid Medicine",
            quantity=10,
            expiry_date=date.today() + timedelta(days=30),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.days_until_expiry() == 30

    def test_days_until_expiry_negative(self):
        """Test days_until_expiry returns negative for expired medicine."""
        medicine = Medicine(
            id="MED001",
            name="Expired Medicine",
            quantity=10,
            expiry_date=date.today() - timedelta(days=5),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.days_until_expiry() == -5

    def test_days_until_expiry_zero(self):
        """Test days_until_expiry returns 0 for medicine expiring today."""
        medicine = Medicine(
            id="MED001",
            name="Expiring Today",
            quantity=10,
            expiry_date=date.today(),
            shelf_id="SHELF-A1",
            price=5.99
        )

        assert medicine.days_until_expiry() == 0

    def test_to_dict_serialization(self):
        """Test Medicine serialization to dictionary."""
        medicine = Medicine(
            id="MED001",
            name="Paracetamol 500mg",
            quantity=100,
            expiry_date=date(2025, 12, 31),
            shelf_id="SHELF-A1",
            price=5.99
        )

        result = medicine.to_dict()

        assert result == {
            "id": "MED001",
            "name": "Paracetamol 500mg",
            "quantity": 100,
            "expiry_date": "2025-12-31",
            "shelf_id": "SHELF-A1",
            "price": 5.99
        }

    def test_from_dict_deserialization(self):
        """Test Medicine deserialization from dictionary."""
        data = {
            "id": "MED001",
            "name": "Paracetamol 500mg",
            "quantity": 100,
            "expiry_date": "2025-12-31",
            "shelf_id": "SHELF-A1",
            "price": 5.99
        }

        medicine = Medicine.from_dict(data)

        assert medicine.id == "MED001"
        assert medicine.name == "Paracetamol 500mg"
        assert medicine.quantity == 100
        assert medicine.expiry_date == date(2025, 12, 31)
        assert medicine.shelf_id == "SHELF-A1"
        assert medicine.price == 5.99

    def test_from_dict_missing_field_raises_error(self):
        """Test from_dict raises KeyError for missing required field."""
        data = {
            "id": "MED001",
            "name": "Paracetamol 500mg",
            # missing quantity
            "expiry_date": "2025-12-31",
            "shelf_id": "SHELF-A1",
            "price": 5.99
        }

        with pytest.raises(KeyError):
            Medicine.from_dict(data)

    def test_from_dict_invalid_date_format_raises_error(self):
        """Test from_dict raises ValueError for invalid date format."""
        data = {
            "id": "MED001",
            "name": "Paracetamol 500mg",
            "quantity": 100,
            "expiry_date": "invalid-date",
            "shelf_id": "SHELF-A1",
            "price": 5.99
        }

        with pytest.raises(ValueError):
            Medicine.from_dict(data)


class TestShelf:
    """Test suite for Shelf class."""

    def test_shelf_creation_valid(self):
        """Test creating a valid Shelf object."""
        shelf = Shelf(
            id="SHELF-A1",
            row="A",
            column="1",
            capacity="100"
        )

        assert shelf.id == "SHELF-A1"
        assert shelf.row == "A"
        assert shelf.column == "1"
        assert shelf.capacity == "100"

    def test_shelf_to_dict_serialization(self):
        """Test Shelf serialization to dictionary."""
        shelf = Shelf(
            id="SHELF-A1",
            row="A",
            column="1",
            capacity="100"
        )

        result = shelf.to_dict()

        assert result == {
            "id": "SHELF-A1",
            "row": "A",
            "column": "1",
            "capacity": "100"
        }

    def test_shelf_from_dict_deserialization(self):
        """Test Shelf deserialization from dictionary."""
        data = {
            "id": "SHELF-A1",
            "row": "A",
            "column": "1",
            "capacity": "100"
        }

        shelf = Shelf.from_dict(data)

        assert shelf.id == "SHELF-A1"
        assert shelf.row == "A"
        assert shelf.column == "1"
        assert shelf.capacity == "100"

    def test_shelf_from_dict_missing_field_raises_error(self):
        """Test from_dict raises KeyError for missing required field."""
        data = {
            "id": "SHELF-A1",
            "row": "A",
            # missing column
            "capacity": "100"
        }

        with pytest.raises(KeyError):
            Shelf.from_dict(data)
