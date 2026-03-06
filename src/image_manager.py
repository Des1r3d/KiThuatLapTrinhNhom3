"""
Image Manager for Pharmacy Management System.

Handles medicine image operations:
- Copy images to local storage (data/images/)
- Generate unique filenames based on medicine ID
- Validate image files (format, size)
- Delete images when medicines are removed
"""
import os
import shutil
from pathlib import Path
from typing import Optional, List

# Supported image formats
SUPPORTED_FORMATS: List[str] = [".png", ".jpg", ".jpeg", ".bmp", ".webp"]

# Maximum image file size in bytes (5MB)
MAX_IMAGE_SIZE: int = 5 * 1024 * 1024

# Default images directory
DEFAULT_IMAGES_DIR: str = "data/images"


class ImageManager:
    """
    Manages medicine images in local filesystem.

    Images are stored in a dedicated directory (data/images/) with
    filenames based on medicine IDs for easy lookup.

    Attributes:
        images_dir: Path to images directory
    """

    def __init__(self, images_dir: str = DEFAULT_IMAGES_DIR):
        """
        Initialize ImageManager.

        Args:
            images_dir: Path to directory where images will be stored
        """
        self.images_dir = images_dir
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create images directory if it doesn't exist."""
        Path(self.images_dir).mkdir(parents=True, exist_ok=True)

    def validate_image(self, source_path: str) -> None:
        """
        Validate an image file before importing.

        Args:
            source_path: Path to image file to validate

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported
            ValueError: If file size exceeds limit
        """
        path = Path(source_path)

        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {source_path}")

        # Check format
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED_FORMATS:
            formats_str = ", ".join(SUPPORTED_FORMATS)
            raise ValueError(
                f"Unsupported image format: '{suffix}'. "
                f"Supported formats: {formats_str}"
            )

        # Check file size
        file_size = path.stat().st_size
        if file_size > MAX_IMAGE_SIZE:
            max_mb = MAX_IMAGE_SIZE / (1024 * 1024)
            actual_mb = file_size / (1024 * 1024)
            raise ValueError(
                f"Image file too large: {actual_mb:.1f}MB. "
                f"Maximum allowed: {max_mb:.0f}MB"
            )

    def save_image(self, source_path: str, medicine_id: str) -> str:
        """
        Copy an image to the images directory with a medicine-ID-based name.

        Args:
            source_path: Path to source image file
            medicine_id: Medicine ID to use as filename base

        Returns:
            Relative path to saved image (relative to images_dir parent)

        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If image is invalid (format/size)
            IOError: If copy operation fails
        """
        self.validate_image(source_path)

        source = Path(source_path)
        ext = source.suffix.lower()

        # Generate filename: medicine_id + extension
        # Sanitize medicine_id for filesystem safety
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")
        filename = f"{safe_id}{ext}"
        dest_path = Path(self.images_dir) / filename

        # Remove existing image for this medicine (different extension possible)
        self.delete_image(medicine_id)

        try:
            shutil.copy2(str(source), str(dest_path))
        except Exception as e:
            raise IOError(f"Failed to save image: {str(e)}") from e

        # Return relative path from data/ parent
        return str(Path(self.images_dir).name / Path(filename))

    def delete_image(self, medicine_id: str) -> bool:
        """
        Delete image(s) associated with a medicine ID.

        Removes any file in images_dir matching the medicine ID
        (regardless of extension).

        Args:
            medicine_id: Medicine ID whose image should be deleted

        Returns:
            True if an image was deleted, False if none found
        """
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")
        deleted = False

        for ext in SUPPORTED_FORMATS:
            image_path = Path(self.images_dir) / f"{safe_id}{ext}"
            if image_path.exists():
                try:
                    image_path.unlink()
                    deleted = True
                except OSError:
                    pass

        return deleted

    def get_image_path(self, medicine_id: str) -> Optional[str]:
        """
        Get the absolute path to a medicine's image if it exists.

        Args:
            medicine_id: Medicine ID to look up

        Returns:
            Absolute path to image file, or None if no image exists
        """
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")

        for ext in SUPPORTED_FORMATS:
            image_path = Path(self.images_dir) / f"{safe_id}{ext}"
            if image_path.exists():
                return str(image_path.resolve())

        return None

    def get_image_path_from_relative(self, relative_path: str) -> Optional[str]:
        """
        Resolve a relative image path to absolute path.

        Args:
            relative_path: Relative path stored in Medicine.image_path

        Returns:
            Absolute path if file exists, None otherwise
        """
        if not relative_path:
            return None

        # Try relative to the images_dir parent
        abs_path = Path(self.images_dir).parent / relative_path
        if abs_path.exists():
            return str(abs_path.resolve())

        return None

    def image_exists(self, medicine_id: str) -> bool:
        """
        Check if a medicine has an associated image.

        Args:
            medicine_id: Medicine ID to check

        Returns:
            True if image exists, False otherwise
        """
        return self.get_image_path(medicine_id) is not None
