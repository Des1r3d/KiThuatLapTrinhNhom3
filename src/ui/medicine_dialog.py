"""
Medicine Dialog for adding/editing medicines.

Provides a form dialog with:
- Input validation
- Shelf selection
- Auto-ID generation
- Edit mode support
"""
from datetime import date, timedelta
from typing import Optional, List

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit,
    QComboBox, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from src.models import Medicine, Shelf
from src.ui.theme import Theme


class MedicineDialog(QDialog):
    """
    Dialog for adding or editing medicine entries.
    
    Features:
    - Form validation
    - Auto ID generation (UUID)
    - Shelf dropdown populated from available shelves
    - Warning for past expiry dates
    - Confirmation for medicines with existing stock when deleting
    """
    
    def __init__(
        self, 
        parent=None, 
        medicine: Optional[Medicine] = None,
        shelves: Optional[List[Shelf]] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize Medicine Dialog.
        
        Args:
            parent: Parent widget
            medicine: Medicine object to edit (None for Add mode)
            shelves: List of available shelves
            theme: Theme instance for styling
        """
        super().__init__(parent)
        
        self.medicine = medicine
        self.shelves = shelves or []
        self.theme = theme or Theme()
        self.is_edit_mode = medicine is not None
        
        self.setup_ui()
        self.apply_theme()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI components."""
        # Window properties
        title = "Sửa Thuốc" if self.is_edit_mode else "Thêm Thuốc Mới"
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
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
        
        # ID Field (read-only in edit mode, hidden in add mode)
        self.id_input = QLineEdit()
        if self.is_edit_mode:
            self.id_input.setReadOnly(True)
            self.id_input.setPlaceholderText("ID tự động")
            form_layout.addRow("ID:", self.id_input)
        
        # Name Field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ví dụ: Paracetamol 500mg")
        form_layout.addRow("Tên thuốc*:", self.name_input)
        
        # Quantity Field
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setValue(0)
        self.quantity_input.setSuffix(" đơn vị")
        form_layout.addRow("Số lượng*:", self.quantity_input)
        
        # Expiry Date Field
        self.expiry_input = QDateEdit()
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDisplayFormat("dd/MM/yyyy")
        # Default to 1 year from now
        default_expiry = QDate.currentDate().addYears(1)
        self.expiry_input.setDate(default_expiry)
        self.expiry_input.setMinimumDate(QDate.currentDate())
        form_layout.addRow("Hạn sử dụng*:", self.expiry_input)
        
        # Price Field
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0.0)
        self.price_input.setMaximum(9999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setValue(0.0)
        self.price_input.setSuffix(" VNĐ")
        form_layout.addRow("Giá*:", self.price_input)
        
        # Shelf Selection
        self.shelf_combo = QComboBox()
        self.populate_shelves()
        form_layout.addRow("Kệ thuốc*:", self.shelf_combo)
        
        layout.addLayout(form_layout)
        
        # Validation message label
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
        
        self.cancel_button = QPushButton("Hủy")
        self.cancel_button.setProperty("secondary", True)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        save_text = "Cập nhật" if self.is_edit_mode else "Thêm thuốc"
        self.save_button = QPushButton(save_text)
        self.save_button.clicked.connect(self.validate_and_save)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def populate_shelves(self):
        """Populate shelf dropdown with available shelves."""
        self.shelf_combo.clear()
        
        if not self.shelves:
            self.shelf_combo.addItem("Chưa có kệ nào", None)
            self.shelf_combo.setEnabled(False)
            return
        
        for shelf in self.shelves:
            display_text = f"{shelf.id} - Dãy {shelf.row}, Cột {shelf.column}"
            self.shelf_combo.addItem(display_text, shelf.id)
    
    def populate_fields(self):
        """Populate form fields with existing medicine data (Edit mode)."""
        if not self.medicine:
            return
        
        self.id_input.setText(self.medicine.id)
        self.name_input.setText(self.medicine.name)
        self.quantity_input.setValue(self.medicine.quantity)
        
        # Set expiry date
        expiry_qdate = QDate(
            self.medicine.expiry_date.year,
            self.medicine.expiry_date.month,
            self.medicine.expiry_date.day
        )
        self.expiry_input.setDate(expiry_qdate)
        
        self.price_input.setValue(self.medicine.price)
        
        # Set shelf selection
        for i in range(self.shelf_combo.count()):
            if self.shelf_combo.itemData(i) == self.medicine.shelf_id:
                self.shelf_combo.setCurrentIndex(i)
                break
    
    def validate_and_save(self):
        """Validate form input and save medicine."""
        # Clear previous validation message
        self.validation_label.hide()
        
        # Validate required fields
        name = self.name_input.text().strip()
        if not name:
            self.show_validation_error("Vui lòng nhập tên thuốc")
            self.name_input.setFocus()
            return
        
        quantity = self.quantity_input.value()
        price = self.price_input.value()
        
        # Get shelf ID
        shelf_id = self.shelf_combo.currentData()
        if shelf_id is None:
            self.show_validation_error("Vui lòng chọn kệ thuốc")
            return
        
        # Get expiry date
        qdate = self.expiry_input.date()
        expiry_date = date(qdate.year(), qdate.month(), qdate.day())
        
        # Warn if expiry date is in the past or very soon
        days_until_expiry = (expiry_date - date.today()).days
        if days_until_expiry < 0:
            reply = QMessageBox.warning(
                self,
                "Cảnh báo",
                f"Ngày hết hạn đã qua ({abs(days_until_expiry)} ngày). "
                "Bạn có chắc muốn tiếp tục?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        elif days_until_expiry < 30:
            reply = QMessageBox.warning(
                self,
                "Cảnh báo",
                f"Thuốc sẽ hết hạn trong {days_until_expiry} ngày. "
                "Bạn có chắc muốn tiếp tục?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Warn if quantity is very large
        if quantity > 9999:
            reply = QMessageBox.question(
                self,
                "Xác nhận",
                f"Số lượng rất lớn ({quantity} đơn vị). "
                "Vui lòng xác nhận đây không phải lỗi nhập liệu.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                self.quantity_input.setFocus()
                return
        
        # Create medicine object
        try:
            if self.is_edit_mode:
                # Keep existing ID
                medicine_id = self.medicine.id
            else:
                # ID will be auto-generated by InventoryManager
                medicine_id = ""
            
            self.result_medicine = Medicine(
                id=medicine_id,
                name=name,
                quantity=quantity,
                expiry_date=expiry_date,
                shelf_id=shelf_id,
                price=price
            )
            
            self.accept()
            
        except ValueError as e:
            self.show_validation_error(f"Lỗi dữ liệu: {str(e)}")
    
    def show_validation_error(self, message: str):
        """
        Display validation error message.
        
        Args:
            message: Error message to display
        """
        self.validation_label.setText(f"❌ {message}")
        self.validation_label.show()
    
    def apply_theme(self):
        """Apply theme stylesheet to dialog."""
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def get_medicine(self) -> Optional[Medicine]:
        """
        Get the created/edited medicine object.
        
        Returns:
            Medicine object if dialog was accepted, None otherwise
        """
        return getattr(self, 'result_medicine', None)
