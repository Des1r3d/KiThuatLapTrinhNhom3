"""
Storage engine for atomic JSON file operations.

This module handles reading and writing JSON files with:
- Atomic writes (temp file -> rename) to prevent corruption
- Backup/restore mechanism for data safety
- Error handling for corrupted files
"""
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any


class StorageEngine:
    """
    Handles atomic JSON read/write operations with backup mechanism.

    Flow for write_json():
        1. Create backup of existing file (if exists)
        2. Write data to temporary file (.tmp)
        3. Rename temporary file to target filename (atomic operation)
        4. Keep backup for recovery

    Flow for read_json():
        1. Check if file exists
        2. Try to load JSON from file
        3. If corrupted, attempt to restore from backup
        4. Return parsed data or raise appropriate error
    """

    def write_json(self, filepath: str, data: Dict[str, Any]) -> None:
        """
        Write data to JSON file using atomic write operation.

        Args:
            filepath: Path to JSON file
            data: Dictionary to serialize

        Raises:
            IOError: If write operation fails
            OSError: If file operations fail
        """
        filepath_obj = Path(filepath)
        backup_path = Path(f"{filepath}.backup")
        temp_path = Path(f"{filepath}.tmp")

        # Create parent directories if they don't exist
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)

        # Step 1: Create backup of existing file
        if filepath_obj.exists():
            shutil.copy2(filepath_obj, backup_path)

        try:
            # Step 2: Write to temporary file
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Step 3: Atomic rename
            # On Windows, need to remove target first if it exists
            if os.name == 'nt' and filepath_obj.exists():
                filepath_obj.unlink()

            temp_path.rename(filepath_obj)

        except Exception as e:
            # Restore from backup if write failed
            if backup_path.exists() and not filepath_obj.exists():
                shutil.copy2(backup_path, filepath_obj)

            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()

            raise IOError(f"Failed to write JSON file {filepath}: {str(e)}") from e

    def read_json(self, filepath: str) -> Dict[str, Any]:
        """
        Read data from JSON file with automatic backup recovery.

        If the main file is corrupted, attempts to restore from backup.

        Args:
            filepath: Path to JSON file

        Returns:
            Dictionary with loaded data

        Raises:
            FileNotFoundError: If file doesn't exist and no backup found
            json.JSONDecodeError: If JSON is malformed and no backup found
        """
        filepath_obj = Path(filepath)
        backup_path = Path(f"{filepath}.backup")

        # Check if file exists
        if not filepath_obj.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            # Try to read main file
            with open(filepath_obj, 'r', encoding='utf-8') as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            # Main file is corrupted, try backup
            if backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Restore from backup
                    shutil.copy2(backup_path, filepath_obj)
                    return data

                except json.JSONDecodeError:
                    # Backup is also corrupted
                    raise json.JSONDecodeError(
                        f"Both main file and backup are corrupted: {filepath}",
                        e.doc,
                        e.pos
                    ) from e
            else:
                # No backup available
                raise
