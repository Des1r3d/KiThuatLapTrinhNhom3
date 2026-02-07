"""
Test suite for StorageEngine.
Tests cover JSON read/write operations, atomic writes, backup/restore, and error handling.
"""
import pytest
import json
import os
from pathlib import Path
from src.storage import StorageEngine


class TestStorageEngine:
    """Test suite for StorageEngine class."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for test files."""
        return tmp_path

    @pytest.fixture
    def storage_engine(self):
        """Create a StorageEngine instance."""
        return StorageEngine()

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing."""
        return {
            "medicines": [
                {
                    "id": "MED001",
                    "name": "Paracetamol",
                    "quantity": 100,
                    "expiry_date": "2025-12-31",
                    "shelf_id": "A1",
                    "price": 5.99
                }
            ]
        }

    def test_write_json_creates_file(self, storage_engine, temp_dir, sample_data):
        """Test that write_json creates a file with correct data."""
        filepath = temp_dir / "test.json"

        storage_engine.write_json(str(filepath), sample_data)

        assert filepath.exists()
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        assert loaded_data == sample_data

    def test_write_json_overwrites_existing_file(self, storage_engine, temp_dir, sample_data):
        """Test that write_json overwrites existing file."""
        filepath = temp_dir / "test.json"

        # Write initial data
        initial_data = {"test": "initial"}
        storage_engine.write_json(str(filepath), initial_data)

        # Overwrite with new data
        storage_engine.write_json(str(filepath), sample_data)

        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        assert loaded_data == sample_data

    def test_write_json_creates_backup(self, storage_engine, temp_dir, sample_data):
        """Test that write_json creates backup before writing."""
        filepath = temp_dir / "test.json"
        backup_path = temp_dir / "test.json.backup"

        # Write initial data
        initial_data = {"test": "initial"}
        storage_engine.write_json(str(filepath), initial_data)

        # Write new data (should create backup)
        storage_engine.write_json(str(filepath), sample_data)

        # Backup should exist with old data
        assert backup_path.exists()
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        assert backup_data == initial_data

    def test_write_json_atomic_operation(self, storage_engine, temp_dir, sample_data):
        """Test that write_json uses atomic write (temp file then rename)."""
        filepath = temp_dir / "test.json"
        temp_filepath = temp_dir / "test.json.tmp"

        storage_engine.write_json(str(filepath), sample_data)

        # Temp file should not exist after successful write
        assert not temp_filepath.exists()
        # Final file should exist
        assert filepath.exists()

    def test_read_json_returns_correct_data(self, storage_engine, temp_dir, sample_data):
        """Test that read_json returns correct data."""
        filepath = temp_dir / "test.json"

        # Write data first
        storage_engine.write_json(str(filepath), sample_data)

        # Read it back
        loaded_data = storage_engine.read_json(str(filepath))

        assert loaded_data == sample_data

    def test_read_json_file_not_found_raises_error(self, storage_engine, temp_dir):
        """Test that read_json raises FileNotFoundError for missing file."""
        filepath = temp_dir / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            storage_engine.read_json(str(filepath))

    def test_read_json_malformed_json_raises_error(self, storage_engine, temp_dir):
        """Test that read_json raises JSONDecodeError for corrupted file."""
        filepath = temp_dir / "corrupted.json"

        # Write malformed JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("{invalid json content")

        with pytest.raises(json.JSONDecodeError):
            storage_engine.read_json(str(filepath))

    def test_read_json_with_backup_on_corruption(self, storage_engine, temp_dir, sample_data):
        """Test that read_json can recover from backup when main file is corrupted."""
        filepath = temp_dir / "test.json"
        backup_path = temp_dir / "test.json.backup"

        # Write valid data first (creates backup)
        storage_engine.write_json(str(filepath), sample_data)

        # Create backup manually
        with open(filepath, 'r', encoding='utf-8') as f:
            valid_data = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(valid_data)

        # Corrupt main file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("{corrupted")

        # Should recover from backup
        loaded_data = storage_engine.read_json(str(filepath))
        assert loaded_data == sample_data

    def test_write_json_with_unicode_characters(self, storage_engine, temp_dir):
        """Test that write_json handles unicode characters correctly."""
        filepath = temp_dir / "unicode.json"
        unicode_data = {
            "name": "Thuốc giảm đau",
            "description": "止痛药 💊"
        }

        storage_engine.write_json(str(filepath), unicode_data)
        loaded_data = storage_engine.read_json(str(filepath))

        assert loaded_data == unicode_data

    def test_write_json_creates_parent_directories(self, storage_engine, temp_dir):
        """Test that write_json creates parent directories if they don't exist."""
        filepath = temp_dir / "subdir" / "nested" / "test.json"
        sample_data = {"test": "data"}

        storage_engine.write_json(str(filepath), sample_data)

        assert filepath.exists()
        loaded_data = storage_engine.read_json(str(filepath))
        assert loaded_data == sample_data

    def test_write_json_pretty_format(self, storage_engine, temp_dir, sample_data):
        """Test that write_json formats JSON with indentation for readability."""
        filepath = temp_dir / "test.json"

        storage_engine.write_json(str(filepath), sample_data)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Should have indentation (pretty printed)
        assert '\n' in content
        assert '  ' in content  # Check for indentation

    def test_backup_cleanup_after_successful_write(self, storage_engine, temp_dir, sample_data):
        """Test that backup file is kept after write for safety."""
        filepath = temp_dir / "test.json"
        backup_path = temp_dir / "test.json.backup"

        # Write initial data
        initial_data = {"test": "initial"}
        storage_engine.write_json(str(filepath), initial_data)

        # Write new data
        storage_engine.write_json(str(filepath), sample_data)

        # Backup should exist (kept for safety)
        assert backup_path.exists()
