"""
Test suite for ImageManager.
Tests cover image validation, save, delete, and lookup operations.
"""
import pytest
import os
import tempfile
from pathlib import Path
from src.image_manager import (
    ImageManager, SUPPORTED_FORMATS, MAX_IMAGE_SIZE
)


class TestImageManager:
    """Test suite for ImageManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def images_dir(self, temp_dir):
        """Create images directory inside temp dir."""
        img_dir = os.path.join(temp_dir, "images")
        return img_dir

    @pytest.fixture
    def manager(self, images_dir):
        """Create ImageManager with temporary directory."""
        return ImageManager(images_dir=images_dir)

    @pytest.fixture
    def sample_image(self, temp_dir):
        """Create a small sample PNG file for testing."""
        # Minimal valid PNG: 1x1 pixel
        png_data = (
            b'\x89PNG\r\n\x1a\n'  # PNG signature
            b'\x00\x00\x00\rIHDR'  # IHDR chunk
            b'\x00\x00\x00\x01'    # width=1
            b'\x00\x00\x00\x01'    # height=1
            b'\x08\x02'            # 8-bit RGB
            b'\x00\x00\x00'        # compression, filter, interlace
            b'\x90wS\xde'          # CRC
            b'\x00\x00\x00\x0cIDATx'  # IDAT chunk
            b'\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05'
            b'\x18\xd8N'           # CRC
            b'\x00\x00\x00\x00IEND'  # IEND chunk
            b'\xaeB`\x82'          # CRC
        )
        filepath = os.path.join(temp_dir, "test_medicine.png")
        with open(filepath, 'wb') as f:
            f.write(png_data)
        return filepath

    @pytest.fixture
    def sample_jpg(self, temp_dir):
        """Create a small sample JPG file for testing."""
        # Minimal JFIF/JPEG
        jpg_data = (
            b'\xff\xd8\xff\xe0'  # SOI + APP0 marker
            b'\x00\x10JFIF\x00'  # JFIF header
            b'\x01\x01\x00\x00\x01\x00\x01\x00\x00'
            b'\xff\xd9'          # EOI
        )
        filepath = os.path.join(temp_dir, "test_medicine.jpg")
        with open(filepath, 'wb') as f:
            f.write(jpg_data)
        return filepath

    # === Initialization Tests ===

    def test_creates_directory_on_init(self, images_dir):
        """Test that ImageManager creates images directory on init."""
        assert not os.path.exists(images_dir)
        ImageManager(images_dir=images_dir)
        assert os.path.isdir(images_dir)

    def test_does_not_fail_if_directory_exists(self, images_dir):
        """Test that ImageManager works if directory already exists."""
        os.makedirs(images_dir)
        manager = ImageManager(images_dir=images_dir)
        assert os.path.isdir(manager.images_dir)

    # === Validation Tests ===

    def test_validate_valid_png(self, manager, sample_image):
        """Test validation passes for valid PNG file."""
        manager.validate_image(sample_image)  # Should not raise

    def test_validate_valid_jpg(self, manager, sample_jpg):
        """Test validation passes for valid JPG file."""
        manager.validate_image(sample_jpg)  # Should not raise

    def test_validate_missing_file_raises_error(self, manager):
        """Test validation raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            manager.validate_image("/nonexistent/image.png")

    def test_validate_unsupported_format_raises_error(self, manager, temp_dir):
        """Test validation raises ValueError for unsupported format."""
        txt_file = os.path.join(temp_dir, "notes.txt")
        with open(txt_file, 'w') as f:
            f.write("not an image")

        with pytest.raises(ValueError, match="Unsupported image format"):
            manager.validate_image(txt_file)

    def test_validate_oversized_file_raises_error(self, manager, temp_dir):
        """Test validation raises ValueError for files exceeding size limit."""
        large_file = os.path.join(temp_dir, "large.png")
        with open(large_file, 'wb') as f:
            f.write(b'\x00' * (MAX_IMAGE_SIZE + 1))

        with pytest.raises(ValueError, match="Image file too large"):
            manager.validate_image(large_file)

    def test_validate_exact_max_size_passes(self, manager, temp_dir):
        """Test validation passes for file exactly at size limit."""
        exact_file = os.path.join(temp_dir, "exact.png")
        with open(exact_file, 'wb') as f:
            f.write(b'\x00' * MAX_IMAGE_SIZE)

        manager.validate_image(exact_file)  # Should not raise

    # === Save Tests ===

    def test_save_image_copies_file(self, manager, sample_image, images_dir):
        """Test save_image copies file to images directory."""
        rel_path = manager.save_image(sample_image, "MED-001")
        
        # File should exist in images dir
        expected_file = os.path.join(images_dir, "MED-001.png")
        assert os.path.exists(expected_file)

    def test_save_image_returns_relative_path(self, manager, sample_image):
        """Test save_image returns relative path."""
        rel_path = manager.save_image(sample_image, "MED-001")
        
        assert "MED-001.png" in rel_path
        assert "images" in rel_path

    def test_save_image_replaces_existing(self, manager, sample_image, sample_jpg, images_dir):
        """Test save_image replaces existing image for same medicine."""
        manager.save_image(sample_image, "MED-001")
        assert os.path.exists(os.path.join(images_dir, "MED-001.png"))
        
        # Save a JPG for same medicine
        manager.save_image(sample_jpg, "MED-001")
        
        # Old PNG should be removed
        assert not os.path.exists(os.path.join(images_dir, "MED-001.png"))
        # New JPG should exist
        assert os.path.exists(os.path.join(images_dir, "MED-001.jpg"))

    def test_save_image_invalid_file_raises_error(self, manager, temp_dir):
        """Test save_image raises error for invalid image."""
        txt_file = os.path.join(temp_dir, "not_image.txt")
        with open(txt_file, 'w') as f:
            f.write("text")

        with pytest.raises(ValueError):
            manager.save_image(txt_file, "MED-001")

    def test_save_image_sanitizes_id(self, manager, sample_image, images_dir):
        """Test save_image sanitizes medicine ID for filesystem."""
        rel_path = manager.save_image(sample_image, "MED/001\\test")
        
        expected_file = os.path.join(images_dir, "MED_001_test.png")
        assert os.path.exists(expected_file)

    # === Delete Tests ===

    def test_delete_image_removes_file(self, manager, sample_image, images_dir):
        """Test delete_image removes the image file."""
        manager.save_image(sample_image, "MED-001")
        assert os.path.exists(os.path.join(images_dir, "MED-001.png"))
        
        result = manager.delete_image("MED-001")
        
        assert result is True
        assert not os.path.exists(os.path.join(images_dir, "MED-001.png"))

    def test_delete_image_nonexistent_returns_false(self, manager):
        """Test delete_image returns False when no image found."""
        result = manager.delete_image("MED-NONEXISTENT")
        assert result is False

    def test_delete_image_all_formats(self, manager, sample_image, sample_jpg, images_dir):
        """Test delete_image removes files regardless of format."""
        # Save PNG
        manager.save_image(sample_image, "MED-001")
        # Save JPG for another medicine
        manager.save_image(sample_jpg, "MED-002")
        
        manager.delete_image("MED-001")
        assert not os.path.exists(os.path.join(images_dir, "MED-001.png"))
        
        manager.delete_image("MED-002")
        assert not os.path.exists(os.path.join(images_dir, "MED-002.jpg"))

    # === Lookup Tests ===

    def test_get_image_path_existing(self, manager, sample_image):
        """Test get_image_path returns absolute path for existing image."""
        manager.save_image(sample_image, "MED-001")
        
        result = manager.get_image_path("MED-001")
        
        assert result is not None
        assert os.path.isabs(result)
        assert os.path.exists(result)

    def test_get_image_path_nonexistent(self, manager):
        """Test get_image_path returns None for missing image."""
        result = manager.get_image_path("MED-NOIMAGE")
        assert result is None

    def test_image_exists_true(self, manager, sample_image):
        """Test image_exists returns True when image exists."""
        manager.save_image(sample_image, "MED-001")
        assert manager.image_exists("MED-001") is True

    def test_image_exists_false(self, manager):
        """Test image_exists returns False when no image."""
        assert manager.image_exists("MED-001") is False

    def test_get_image_path_from_relative(self, manager, sample_image, images_dir):
        """Test resolving relative path to absolute path."""
        rel_path = manager.save_image(sample_image, "MED-001")

        result = manager.get_image_path_from_relative(rel_path)
        
        assert result is not None
        assert os.path.exists(result)

    def test_get_image_path_from_relative_empty(self, manager):
        """Test resolving empty relative path returns None."""
        result = manager.get_image_path_from_relative("")
        assert result is None

    def test_get_image_path_from_relative_invalid(self, manager):
        """Test resolving nonexistent relative path returns None."""
        result = manager.get_image_path_from_relative("images/nonexistent.png")
        assert result is None
