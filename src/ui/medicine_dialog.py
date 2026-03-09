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
    QComboBox, QPushButton, QLabel, QMessageBox,
    QFileDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap

from src.models import Medicine, Shelf
from src.ui.theme import Theme
from src.image_manager import ImageManager, SUPPORTED_FORMATS


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
        theme: Optional[Theme] = None,
        image_manager: Optional[ImageManager] = None
    ):
        """
        Initialize Medicine Dialog.
        
        Args:
            parent: Parent widget
            medicine: Medicine object to edit (None for Add mode)
            shelves: List of available shelves
            theme: Theme instance for styling
            image_manager: ImageManager instance for image operations
        """
        super().__init__(parent)
        
        self.medicine = medicine
        self.shelves = shelves or []
        self.theme = theme or Theme()
        self.image_manager = image_manager or ImageManager()
        self.is_edit_mode = medicine is not None
        self.selected_image_path: Optional[str] = None  # Source path of newly selected image
        self.image_removed: bool = False  # Flag to track if user removed existing image
        
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
        
        # --- Image upload section ---
        image_section_layout = QVBoxLayout()
        
        # Image preview
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(200, 200)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet(
            "border: 2px dashed #ccc; border-radius: 8px; "
            "background-color: #f9f9f9;"
        )
        self.image_preview.setText("Chưa có ảnh")
        self.image_preview.setScaledContents(False)
        image_section_layout.addWidget(
            self.image_preview, alignment=Qt.AlignmentFlag.AlignCenter
        )
        
        # Image buttons
        image_buttons_layout = QHBoxLayout()
        image_buttons_layout.setSpacing(Theme.SPACING_BASE)
        
        self.upload_button = QPushButton("📷 Chọn ảnh")
        self.upload_button.clicked.connect(self.select_image)
        image_buttons_layout.addWidget(self.upload_button)
        
        self.remove_image_button = QPushButton("🗑️ Xóa ảnh")
        self.remove_image_button.clicked.connect(self.remove_image)
        self.remove_image_button.setEnabled(False)
        image_buttons_layout.addWidget(self.remove_image_button)
        
        image_section_layout.addLayout(image_buttons_layout)
        
        form_layout.addRow("Ảnh thuốc:", image_section_layout)
        
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
            display_text = f"{shelf.id} - Khu {shelf.zone}, Cột {shelf.column}, Dãy {shelf.row}"
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
        
        # Load existing image
        if self.medicine.image_path:
            abs_path = self.image_manager.get_image_path_from_relative(
                self.medicine.image_path
            )
            if abs_path:
                self._display_image(abs_path)
                self.remove_image_button.setEnabled(True)
    
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
            
            # Determine image_path
            image_path = ""
            if self.selected_image_path:
                # New image selected - will be saved by caller
                image_path = "__pending__"  # Placeholder, resolved after save_image
            elif self.is_edit_mode and not self.image_removed:
                # Keep existing image path
                image_path = self.medicine.image_path if self.medicine.image_path else ""
            # else: image_removed=True or no image -> empty string
            
            self.result_medicine = Medicine(
                id=medicine_id,
                name=name,
                quantity=quantity,
                expiry_date=expiry_date,
                shelf_id=shelf_id,
                price=price,
                image_path=image_path
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
    
    def get_selected_image_path(self) -> Optional[str]:
        """
        Get the path of the newly selected image.
        
        Returns:
            Source path of selected image, or None
        """
        return self.selected_image_path
    
    def is_image_removed(self) -> bool:
        """
        Check if user chose to remove the existing image.
        
        Returns:
            True if image was explicitly removed
        """
        return self.image_removed
    
    def select_image(self):
        """
        Open file dialog to select an image.
        
        Validates format and size before accepting.
        """
        formats_filter = " ".join(f"*{fmt}" for fmt in SUPPORTED_FORMATS)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh thuốc",
            "",
            f"Ảnh ({formats_filter});;Tất cả (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            self.image_manager.validate_image(file_path)
        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "Lỗi ảnh", str(e))
            return
        
        self.selected_image_path = file_path
        self.image_removed = False
        self._display_image(file_path)
        self.remove_image_button.setEnabled(True)
    
    def remove_image(self):
        """Remove the current image."""
        self.selected_image_path = None
        self.image_removed = True
        self.image_preview.setPixmap(QPixmap())  # Clear pixmap
        self.image_preview.setText("Chưa có ảnh")
        self.image_preview.setStyleSheet(
            "border: 2px dashed #ccc; border-radius: 8px; "
            "background-color: #f9f9f9;"
        )
        self.remove_image_button.setEnabled(False)
    
    def _display_image(self, image_path: str):
        """
        Display an image in the preview label.
        
        Args:
            image_path: Absolute path to image file
        """
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_preview.setText("Không thể tải ảnh")
            return
        
        # Scale to fit preview area while keeping aspect ratio
        scaled = pixmap.scaled(
            196, 196,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_preview.setPixmap(scaled)
        self.image_preview.setText("")  # Clear placeholder text
        self.image_preview.setStyleSheet(
            "border: 2px solid #4A90D9; border-radius: 8px;"
        )
