"""
Shelf Dialog for adding/editing shelves.

Provides a form dialog with:
- Input validation
- Edit mode support
- Row/Column/Capacity input
"""
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.models import Shelf
from src.ui.theme import Theme


class ShelfDialog(QDialog):
    """
    Dialog for adding or editing shelf entries.
    
    Features:
    - Form validation (ID, Row, Column required)
    - Capacity input with QSpinBox
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
        self.apply_theme()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI components."""
        title = "Sửa Kệ Thuốc" if self.is_edit_mode else "Thêm Kệ Thuốc Mới"
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_BASE * 2)
        layout.setContentsMargins(
            Theme.DIALOG_PADDING,
            Theme.DIALOG_PADDING,
            Theme.DIALOG_PADDING,
            Theme.DIALOG_PADDING
        )
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H1)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(Theme.SPACING_BASE * 2)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # ID Field (read-only, auto-generated)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Tự động tạo từ Khu-Cột+Dãy")
        self.id_input.setReadOnly(True)
        form_layout.addRow("Mã kệ:", self.id_input)
        
        # Zone Field (Khu)
        self.zone_input = QLineEdit()
        self.zone_input.setPlaceholderText("Ví dụ: K")
        self.zone_input.setMaxLength(10)
        if self.is_edit_mode:
            self.zone_input.setReadOnly(True)
        self.zone_input.textChanged.connect(self._update_shelf_id)
        form_layout.addRow("Khu*:", self.zone_input)
        
        # Column Field (Cột)
        self.column_input = QLineEdit()
        self.column_input.setPlaceholderText("Ví dụ: A, B, C")
        self.column_input.setMaxLength(10)
        if self.is_edit_mode:
            self.column_input.setReadOnly(True)
        self.column_input.textChanged.connect(self._update_shelf_id)
        form_layout.addRow("Cột*:", self.column_input)
        
        # Row Field (Dãy)
        self.row_input = QLineEdit()
        self.row_input.setPlaceholderText("Ví dụ: 1, 2, 3")
        self.row_input.setMaxLength(10)
        if self.is_edit_mode:
            self.row_input.setReadOnly(True)
        self.row_input.textChanged.connect(self._update_shelf_id)
        form_layout.addRow("Dãy*:", self.row_input)
        
        # Capacity Field
        self.capacity_input = QSpinBox()
        self.capacity_input.setMinimum(1)
        self.capacity_input.setMaximum(9999)
        self.capacity_input.setValue(50)
        self.capacity_input.setSuffix(" đơn vị")
        form_layout.addRow("Sức chứa*:", self.capacity_input)
        
        layout.addLayout(form_layout)
        
        # Validation message
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet("color: #C0392B; font-size: 12px;")
        self.validation_label.setWordWrap(True)
        self.validation_label.hide()
        layout.addWidget(self.validation_label)
        
        # Required fields note
        note_label = QLabel("* Trường bắt buộc")
        note_label.setProperty("secondary", True)
        layout.addWidget(note_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Hủy")
        cancel_button.setProperty("secondary", True)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_text = "Cập nhật" if self.is_edit_mode else "Thêm kệ"
        self.save_button = QPushButton(save_text)
        self.save_button.clicked.connect(self.validate_and_save)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _update_shelf_id(self):
        """Auto-generate shelf ID from zone, column, and row inputs."""
        zone = self.zone_input.text().strip().upper()
        column = self.column_input.text().strip().upper()
        row = self.row_input.text().strip()
        if zone and column and row:
            self.id_input.setText(f"{zone}-{column}{row}")
        else:
            self.id_input.setText("")
    
    def populate_fields(self):
        """Populate form fields with existing shelf data (Edit mode)."""
        if not self.shelf:
            return
        
        self.zone_input.setText(self.shelf.zone)
        self.column_input.setText(self.shelf.column)
        self.row_input.setText(self.shelf.row)
        # ID is auto-generated from zone/column/row via _update_shelf_id
        
        try:
            self.capacity_input.setValue(int(self.shelf.capacity))
        except ValueError:
            self.capacity_input.setValue(50)
    
    def show_validation_error(self, message: str):
        """Display validation error message."""
        self.validation_label.setText(f"❌ {message}")
        self.validation_label.show()
    
    def validate_and_save(self):
        """Validate form input and create Shelf object."""
        self.validation_label.hide()
        
        zone = self.zone_input.text().strip().upper()
        if not zone:
            self.show_validation_error("Vui lòng nhập khu")
            self.zone_input.setFocus()
            return
        
        column = self.column_input.text().strip().upper()
        if not column:
            self.show_validation_error("Vui lòng nhập cột")
            self.column_input.setFocus()
            return
        
        row = self.row_input.text().strip()
        if not row:
            self.show_validation_error("Vui lòng nhập dãy")
            self.row_input.setFocus()
            return
        
        shelf_id = f"{zone}-{column}{row}"
        capacity = str(self.capacity_input.value())
        
        self.result_shelf = Shelf(
            id=shelf_id,
            zone=zone,
            column=column,
            row=row,
            capacity=capacity
        )
        self.accept()
    
    def get_shelf(self) -> Optional[Shelf]:
        """
        Get the created/edited shelf object.
        
        Returns:
            Shelf object if dialog was accepted, None otherwise
        """
        return self.result_shelf
    
    def apply_theme(self):
        """Apply theme stylesheet to dialog."""
        self.setStyleSheet(self.theme.get_stylesheet())
