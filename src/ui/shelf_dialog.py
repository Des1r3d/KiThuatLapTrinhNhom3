"""
Shelf Dialog for adding/editing shelves.

Uses Qt Designer-generated UI from them_ke.py.
Provides:
- Input validation
- Edit mode support
- Row/Column/Capacity input
"""
from typing import Optional

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt

from src.models import Shelf
from src.ui.theme import Theme
from src.ui.generated.them_ke import Ui_dlg_add_shelf


class ShelfDialog(QDialog):
    """
    Dialog for adding or editing shelf entries.
    
    Uses Ui_dlg_add_shelf from Qt Designer for layout.
    
    Features:
    - Form validation (ID, Row, Column required)
    - Capacity input
    - Edit mode (ID read-only)
    """
    
    def __init__(
        self,
        parent=None,
        shelf: Optional[Shelf] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize Shelf Dialog.
        
        Args:
            parent: Parent widget
            shelf: Shelf object to edit (None for Add mode)
            theme: Theme instance for styling
        """
        super().__init__(parent)
        
        self.shelf = shelf
        self.theme = theme or Theme()
        self.is_edit_mode = shelf is not None
        self.result_shelf: Optional[Shelf] = None
        
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        self.ui = Ui_dlg_add_shelf()
        self.ui.setupUi(self)
        
        # Set window title based on mode
        title = "Sửa Kệ Thuốc" if self.is_edit_mode else "Thêm Kệ Thuốc Mới"
        self.setWindowTitle(title)
        self.ui.lbl_title.setText(title)
        
        # Connect auto-ID generation
        self.ui.txt_shelf_row.textChanged.connect(self._update_shelf_id)
        self.ui.txt_shelf_col.textChanged.connect(self._update_shelf_id)
        
        # Connect buttons
        self.ui.btn_primary.clicked.connect(self.validate_and_save)
        self.ui.btn_secondary.clicked.connect(self.reject)
        
        # Set button text based on mode
        self.ui.btn_primary.setText("Cập nhật" if self.is_edit_mode else "Save")
        
        # In edit mode, make ID fields read-only
        if self.is_edit_mode:
            self.ui.txt_shelf_id.setReadOnly(True)
            self.ui.txt_shelf_row.setReadOnly(True)
            self.ui.txt_shelf_col.setReadOnly(True)
    
    def _update_shelf_id(self):
        """Auto-generate shelf ID from row and column inputs."""
        shelf_id_text = self.ui.txt_shelf_id.text().strip()
        row = self.ui.txt_shelf_row.text().strip().upper()
        col = self.ui.txt_shelf_col.text().strip()
        
        if row and col:
            # Generate ID as K-{row}{col} format
            self.ui.txt_shelf_id.setText(f"K-{row}{col}")
        elif not self.is_edit_mode:
            self.ui.txt_shelf_id.setText("")
    
    def populate_fields(self):
        """Populate form fields with existing shelf data (Edit mode)."""
        if not self.shelf:
            return
        
        self.ui.txt_shelf_id.setText(self.shelf.id)
        self.ui.txt_shelf_row.setText(self.shelf.row)
        self.ui.txt_shelf_col.setText(self.shelf.column)
        self.ui.txt_shelf_capacity.setText(str(self.shelf.capacity))
    
    def validate_and_save(self):
        """Validate form input and create Shelf object."""
        # Validate shelf ID
        shelf_id = self.ui.txt_shelf_id.text().strip()
        if not shelf_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID kệ")
            self.ui.txt_shelf_id.setFocus()
            return
        
        row = self.ui.txt_shelf_row.text().strip().upper()
        if not row:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập dãy")
            self.ui.txt_shelf_row.setFocus()
            return
        
        col = self.ui.txt_shelf_col.text().strip().upper()
        if not col:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập cột")
            self.ui.txt_shelf_col.setFocus()
            return
        
        # Validate capacity
        capacity_text = self.ui.txt_shelf_capacity.text().strip()
        try:
            capacity = int(capacity_text) if capacity_text else 50
            if capacity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Sức chứa phải là số nguyên dương")
            self.ui.txt_shelf_capacity.setFocus()
            return
        
        # Extract zone from shelf_id (e.g., "K-A1" -> zone="K")
        zone = shelf_id.split("-")[0] if "-" in shelf_id else "K"
        
        self.result_shelf = Shelf(
            id=shelf_id,
            zone=zone,
            column=col,
            row=row,
            capacity=str(capacity)
        )
        self.accept()
    
    def get_shelf(self) -> Optional[Shelf]:
        """Get the created/edited shelf object."""
        return self.result_shelf
    
    def apply_theme(self):
        """Apply theme stylesheet to dialog."""
        pass  # Uses Qt Designer inline styles
