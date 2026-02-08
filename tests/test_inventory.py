"""
Test suite for InventoryManager.
Tests cover CRUD operations, validation, and persistence.
"""
import pytest
import os
import json
import tempfile
from datetime import date, timedelta
from src.models import Medicine, Shelf
from src.inventory_manager import InventoryManager


class TestInventoryManager:
    """Test suite for InventoryManager class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def sample_medicine(self):
        """Create a sample valid medicine."""
        return Medicine(
            id="MED001",
            name="Paracetamol 500mg",
            quantity=100,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    @pytest.fixture
    def sample_shelf(self):
        """Create a sample valid shelf."""
        return Shelf(
            id="SHELF-A1",
            row="A",
            column="1",
            capacity="100"
        )
    
    @pytest.fixture
    def manager(self, temp_dir):
        """Create InventoryManager with temporary file paths."""
        medicines_path = os.path.join(temp_dir, "medicines.json")
        shelves_path = os.path.join(temp_dir, "shelves.json")
        return InventoryManager(
            medicines_filepath=medicines_path,
            shelves_filepath=shelves_path
        )
    
    # === Initialization Tests ===
    
    def test_initialization_empty(self, manager):
        """Test InventoryManager initializes with empty lists."""
        assert manager.medicines == []
        assert manager.shelves == []
    
    def test_load_data_empty_files(self, manager):
        """Test load_data handles missing files gracefully."""
        manager.load_data()
        assert manager.medicines == []
        assert manager.shelves == []
    
    def test_load_data_existing_files(self, temp_dir):
        """Test load_data reads existing JSON files."""
        medicines_path = os.path.join(temp_dir, "medicines.json")
        shelves_path = os.path.join(temp_dir, "shelves.json")
        
        # Create test data files
        medicines_data = [{
            "id": "MED001",
            "name": "Paracetamol",
            "quantity": 50,
            "expiry_date": "2026-12-31",
            "shelf_id": "SHELF-A1",
            "price": 5.99
        }]
        shelves_data = [{
            "id": "SHELF-A1",
            "row": "A",
            "column": "1",
            "capacity": "100"
        }]
        
        os.makedirs(temp_dir, exist_ok=True)
        with open(medicines_path, 'w') as f:
            json.dump(medicines_data, f)
        with open(shelves_path, 'w') as f:
            json.dump(shelves_data, f)
        
        manager = InventoryManager(medicines_path, shelves_path)
        manager.load_data()
        
        assert len(manager.medicines) == 1
        assert manager.medicines[0].name == "Paracetamol"
        assert len(manager.shelves) == 1
        assert manager.shelves[0].id == "SHELF-A1"
    
    # === Add Medicine Tests ===
    
    def test_add_medicine_success(self, manager, sample_medicine):
        """Test adding a medicine successfully."""
        result = manager.add_medicine(sample_medicine)
        
        assert result == sample_medicine
        assert len(manager.medicines) == 1
        assert manager.medicines[0] == sample_medicine
    
    def test_add_medicine_auto_generate_id(self, manager):
        """Test adding medicine with empty ID generates new ID."""
        medicine = Medicine(
            id="",
            name="Test Medicine",
            quantity=10,
            expiry_date=date.today() + timedelta(days=30),
            shelf_id="SHELF-A1",
            price=9.99
        )
        
        result = manager.add_medicine(medicine)
        
        assert result.id.startswith("MED-")
        assert len(result.id) == 12  # "MED-" + 8 chars
        assert result.name == "Test Medicine"
    
    def test_add_medicine_duplicate_id_raises_error(self, manager, sample_medicine):
        """Test adding medicine with duplicate ID raises ValueError."""
        manager.add_medicine(sample_medicine)
        
        with pytest.raises(ValueError, match="already exists"):
            manager.add_medicine(sample_medicine)
    
    def test_add_medicine_invalid_shelf_raises_error(self, manager, sample_shelf):
        """Test adding medicine with invalid shelf_id raises ValueError."""
        # Add a shelf so validation is enforced
        manager.add_shelf(sample_shelf)
        
        medicine = Medicine(
            id="MED002",
            name="Test Medicine",
            quantity=10,
            expiry_date=date.today() + timedelta(days=30),
            shelf_id="INVALID-SHELF",
            price=9.99
        )
        
        with pytest.raises(ValueError, match="does not exist"):
            manager.add_medicine(medicine)
    
    def test_add_medicine_persists_to_file(self, manager, sample_medicine):
        """Test that add_medicine saves to file."""
        manager.add_medicine(sample_medicine)
        
        # Verify file exists and contains data
        assert os.path.exists(manager.medicines_filepath)
        
        with open(manager.medicines_filepath, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]["id"] == "MED001"
    
    def test_add_medicine_no_auto_save(self, manager, sample_medicine):
        """Test add_medicine with auto_save=False doesn't persist."""
        manager.add_medicine(sample_medicine, auto_save=False)
        
        assert len(manager.medicines) == 1
        assert not os.path.exists(manager.medicines_filepath)
    
    # === Remove Medicine Tests ===
    
    def test_remove_medicine_success(self, manager, sample_medicine):
        """Test removing a medicine successfully."""
        manager.add_medicine(sample_medicine)
        
        removed = manager.remove_medicine("MED001")
        
        assert removed == sample_medicine
        assert len(manager.medicines) == 0
    
    def test_remove_medicine_not_found_raises_error(self, manager):
        """Test removing non-existent medicine raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            manager.remove_medicine("INVALID-ID")
    
    def test_remove_medicine_persists_to_file(self, manager, sample_medicine):
        """Test that remove_medicine updates file."""
        manager.add_medicine(sample_medicine)
        manager.remove_medicine("MED001")
        
        with open(manager.medicines_filepath, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 0
    
    # === Update Medicine Tests ===
    
    def test_update_medicine_success(self, manager, sample_medicine):
        """Test updating a medicine successfully."""
        manager.add_medicine(sample_medicine)
        
        updated = manager.update_medicine("MED001", {"quantity": 50, "price": 7.99})
        
        assert updated.id == "MED001"
        assert updated.quantity == 50
        assert updated.price == 7.99
        assert updated.name == sample_medicine.name  # unchanged
    
    def test_update_medicine_not_found_raises_error(self, manager):
        """Test updating non-existent medicine raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            manager.update_medicine("INVALID-ID", {"quantity": 10})
    
    def test_update_medicine_invalid_quantity_raises_error(self, manager, sample_medicine):
        """Test updating with invalid values raises ValueError."""
        manager.add_medicine(sample_medicine)
        
        with pytest.raises(ValueError, match="Quantity must be >= 0"):
            manager.update_medicine("MED001", {"quantity": -5})
    
    def test_update_medicine_immutable_pattern(self, manager, sample_medicine):
        """Test that update creates new object (immutable pattern)."""
        manager.add_medicine(sample_medicine)
        original_id = id(manager.medicines[0])
        
        manager.update_medicine("MED001", {"quantity": 50})
        new_id = id(manager.medicines[0])
        
        assert original_id != new_id
    
    def test_update_medicine_persists_to_file(self, manager, sample_medicine):
        """Test that update_medicine saves to file."""
        manager.add_medicine(sample_medicine)
        manager.update_medicine("MED001", {"quantity": 50})
        
        with open(manager.medicines_filepath, 'r') as f:
            data = json.load(f)
        
        assert data[0]["quantity"] == 50
    
    # === Get Medicine Tests ===
    
    def test_get_medicine_found(self, manager, sample_medicine):
        """Test getting existing medicine."""
        manager.add_medicine(sample_medicine)
        
        result = manager.get_medicine("MED001")
        
        assert result == sample_medicine
    
    def test_get_medicine_not_found(self, manager):
        """Test getting non-existent medicine returns None."""
        result = manager.get_medicine("INVALID-ID")
        
        assert result is None
    
    def test_get_all_medicines(self, manager, sample_medicine):
        """Test getting all medicines."""
        medicine2 = Medicine(
            id="MED002",
            name="Aspirin",
            quantity=50,
            expiry_date=date.today() + timedelta(days=180),
            shelf_id="SHELF-A1",
            price=3.99
        )
        
        manager.add_medicine(sample_medicine, auto_save=False)
        manager.add_medicine(medicine2, auto_save=False)
        
        result = manager.get_all_medicines()
        
        assert len(result) == 2
        assert sample_medicine in result
        assert medicine2 in result
    
    def test_get_all_medicines_returns_copy(self, manager, sample_medicine):
        """Test that get_all_medicines returns a copy, not the original list."""
        manager.add_medicine(sample_medicine)
        
        result = manager.get_all_medicines()
        result.append(sample_medicine)  # Modify the returned list
        
        assert len(manager.medicines) == 1  # Original unchanged
    
    # === Shelf Tests ===
    
    def test_add_shelf_success(self, manager, sample_shelf):
        """Test adding a shelf successfully."""
        result = manager.add_shelf(sample_shelf)
        
        assert result == sample_shelf
        assert len(manager.shelves) == 1
    
    def test_add_shelf_duplicate_id_raises_error(self, manager, sample_shelf):
        """Test adding shelf with duplicate ID raises ValueError."""
        manager.add_shelf(sample_shelf)
        
        with pytest.raises(ValueError, match="already exists"):
            manager.add_shelf(sample_shelf)
    
    def test_get_shelf_found(self, manager, sample_shelf):
        """Test getting existing shelf."""
        manager.add_shelf(sample_shelf)
        
        result = manager.get_shelf("SHELF-A1")
        
        assert result == sample_shelf
    
    def test_get_shelf_not_found(self, manager):
        """Test getting non-existent shelf returns None."""
        result = manager.get_shelf("INVALID-ID")
        
        assert result is None
    
    def test_get_all_shelves(self, manager, sample_shelf):
        """Test getting all shelves."""
        shelf2 = Shelf(id="SHELF-B1", row="B", column="1", capacity="50")
        
        manager.add_shelf(sample_shelf, auto_save=False)
        manager.add_shelf(shelf2, auto_save=False)
        
        result = manager.get_all_shelves()
        
        assert len(result) == 2
    
    # === Integration Tests ===
    
    def test_full_crud_cycle(self, manager, sample_shelf):
        """Test complete Create-Read-Update-Delete cycle."""
        # Add shelf
        manager.add_shelf(sample_shelf)
        
        # Create
        medicine = Medicine(
            id="",
            name="Test Medicine",
            quantity=100,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=9.99
        )
        added = manager.add_medicine(medicine)
        generated_id = added.id
        
        # Read
        retrieved = manager.get_medicine(generated_id)
        assert retrieved is not None
        assert retrieved.name == "Test Medicine"
        
        # Update
        updated = manager.update_medicine(generated_id, {"quantity": 50})
        assert updated.quantity == 50
        
        # Delete
        removed = manager.remove_medicine(generated_id)
        assert removed.id == generated_id
        assert manager.get_medicine(generated_id) is None
    
    def test_persistence_across_instances(self, temp_dir, sample_shelf):
        """Test data persists across manager instances."""
        medicines_path = os.path.join(temp_dir, "medicines.json")
        shelves_path = os.path.join(temp_dir, "shelves.json")
        
        # First instance - add data
        manager1 = InventoryManager(medicines_path, shelves_path)
        manager1.add_shelf(sample_shelf)
        
        medicine = Medicine(
            id="MED001",
            name="Persistent Medicine",
            quantity=100,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=9.99
        )
        manager1.add_medicine(medicine)
        
        # Second instance - load data
        manager2 = InventoryManager(medicines_path, shelves_path)
        manager2.load_data()
        
        assert len(manager2.medicines) == 1
        assert manager2.medicines[0].name == "Persistent Medicine"
