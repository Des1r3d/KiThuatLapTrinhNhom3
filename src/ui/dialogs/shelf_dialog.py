"""
Shelf Dialog — PHARMA.SYS Add/Edit Shelf.

Uses Qt Designer-generated UI from them_ke.py for layout.
Features:
- Auto-generate shelf ID from zone + column (letter) + row (number)
- Input validation: zone (uppercase letters), column/dãy (uppercase letter), 
  row/cột (number)
- Auto uppercase for zone and column inputs
- Add and Edit modes
"""
import re
from typing import Optional, List, Dict, Any

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt

from src.models import Shelf
from src.ui.theme import Theme, ThemeMode
from src.ui.generated.them_ke import Ui_dlg_add_shelf
from src.ui.generated.them_ke_dark import Ui_dlg_add_shelf as Ui_dlg_add_shelf_dark


class ShelfDialog(QDialog):
    """
    Dialog for adding or editing a shelf.

    Uses Ui_dlg_add_shelf from them_ke.py for layout.

    Shelf ID format: {zone}-{column}{row}
    - zone: Uppercase letter(s) representing the zone/area (Khu)
    - column: Uppercase letter(s) (Dãy/Cột A, B, C...)
    - row: Number(s) (Hàng/Cột 1, 2, 3...)

    Example: K-A1 = Zone K, Column A, Row 1

    Attributes:
        mode: 'add' or 'edit'
        shelf: Existing Shelf object (edit mode)
        result_data: Validated Shelf data on accept
    """

    def __init__(
        self,
        parent=None,
        mode: str = "add",
        shelf: Optional[Shelf] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize Shelf Dialog.

        Args:
            parent: Parent widget
            mode: 'add' or 'edit'
            shelf: Shelf object to edit (edit mode only)
            theme: Theme instance for styling
        """
        super().__init__(parent)

        self.mode = mode
        self.shelf = shelf
        self.theme = theme or Theme()
        self.result_data: Optional[Dict[str, Any]] = None

        self.setup_ui()

        if mode == "edit" and shelf:
            self.load_shelf(shelf)

    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        # Choose UI class based on current theme mode
        if self.theme.mode == ThemeMode.DARK:
            self.ui = Ui_dlg_add_shelf_dark()
        else:
            self.ui = Ui_dlg_add_shelf()
        self.ui.setupUi(self)

        # ── Mode-specific setup ──
        if self.mode == "add":
            self.setWindowTitle("Thêm kệ mới")
            self.ui.lbl_title.setText("Thêm kệ")
            self.ui.btn_primary.setText("Thêm")
            self.ui.btn_secondary.setText("Hủy")
        else:
            self.setWindowTitle("Chỉnh sửa kệ")
            self.ui.lbl_title.setText("Chỉnh sửa kệ")
            self.ui.btn_primary.setText("Lưu")
            self.ui.btn_secondary.setText("Hủy")

        # ID field is read-only (auto-generated from zone + column + row)
        self.ui.txt_shelf_id.setReadOnly(True)
        self.ui.txt_shelf_id.setStyleSheet(
            self.ui.txt_shelf_id.styleSheet()
            + " color: #94A3B8; background-color: #F0F2F5;"
        )
        self.ui.txt_shelf_id.setPlaceholderText("Tự động tạo từ Dãy + Cột")

        # ── Connect signals ──
        self.ui.btn_primary.clicked.connect(self.on_save)
        self.ui.btn_secondary.clicked.connect(self.reject)

        # Auto-generate ID when zone/column/row change
        self.ui.txt_shelf_row.textChanged.connect(self._auto_generate_id)
        self.ui.txt_shelf_col.textChanged.connect(self._auto_generate_id)

        # Auto uppercase for row (letter) field
        self.ui.txt_shelf_row.textChanged.connect(
            lambda: self.ui.txt_shelf_row.setText(
                self.ui.txt_shelf_row.text().upper()
            )
        )

    def _auto_generate_id(self):
        """Auto-generate shelf ID from zone + column + row inputs."""
        # In the UI: txt_shelf_row = "Dãy" (letters A,B,C) → model column
        # In the UI: txt_shelf_col = "Cột" (numbers 1,2,3) → model row
        column_letter = self.ui.txt_shelf_row.text().strip().upper()
        row_number = self.ui.txt_shelf_col.text().strip()

        if column_letter and row_number:
            shelf_id = f"K-{column_letter}{row_number}"
            self.ui.txt_shelf_id.setText(shelf_id)
        else:
            self.ui.txt_shelf_id.clear()

    def load_shelf(self, shelf: Shelf):
        """
        Pre-fill dialog fields with shelf data.

        Args:
            shelf: Shelf object to load
        """
        self.shelf = shelf

        self.ui.txt_shelf_id.setText(shelf.id)

        # Map model fields to UI fields
        # model.column (letter) → UI txt_shelf_row ("Dãy")
        # model.row (number) → UI txt_shelf_col ("Cột")
        self.ui.txt_shelf_row.setText(shelf.column)
        self.ui.txt_shelf_col.setText(shelf.row)
        self.ui.txt_shelf_capacity.setText(str(shelf.capacity))

    def on_save(self):
        """Validate inputs and accept dialog."""
        errors = []

        # Column/Dãy (letter part) — UI txt_shelf_row
        column_letter = self.ui.txt_shelf_row.text().strip().upper()
        if not column_letter:
            errors.append("Dãy không được để trống")
        elif not re.match(r'^[A-Z]+$', column_letter):
            errors.append("Dãy phải là chữ cái (VD: A, B, C)")

        # Row/Cột (number part) — UI txt_shelf_col
        row_number = self.ui.txt_shelf_col.text().strip()
        if not row_number:
            errors.append("Cột không được để trống")
        elif not re.match(r'^[0-9]+$', row_number):
            errors.append("Cột phải là số (VD: 1, 2, 3)")

        # Capacity
        capacity_text = self.ui.txt_shelf_capacity.text().strip()
        if not capacity_text:
            errors.append("Sức chứa không được để trống")
        else:
            try:
                capacity = int(capacity_text)
                if capacity <= 0:
                    errors.append("Sức chứa phải lớn hơn 0")
            except ValueError:
                errors.append("Sức chứa phải là số nguyên hợp lệ")

        # Show errors
        if errors:
            error_msg = "\n".join(f"• {e}" for e in errors)
            QMessageBox.warning(
                self,
                "Lỗi nhập liệu",
                f"Vui lòng sửa các lỗi sau:\n\n{error_msg}"
            )
            return

        # Build shelf ID
        zone = "K"  # Default zone
        shelf_id = f"{zone}-{column_letter}{row_number}"

        # Build result data
        self.result_data = {
            "id": shelf_id,
            "zone": zone,
            "column": column_letter,  # Letter part (model.column)
            "row": row_number,        # Number part (model.row)
            "capacity": capacity_text,
        }

        self.accept()

    def get_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the validated form data.

        Returns:
            Dictionary with shelf field values, or None if cancelled
        """
        return self.result_data
