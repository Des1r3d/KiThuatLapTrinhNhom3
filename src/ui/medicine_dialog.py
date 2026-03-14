"""
Medicine Dialog for adding/editing medicines.

Uses Qt Designer-generated UI from them_thuoc.py.
Provides:
- Input validation
- Shelf selection
- Auto-ID generation
- Edit mode support
- Image upload
"""
from datetime import date
from typing import Optional, List

from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap

from src.models import Medicine, Shelf
from src.ui.theme import Theme
from src.image_manager import ImageManager, SUPPORTED_FORMATS
from src.ui.generated.them_thuoc import Ui_dlg_medicine_detail


class MedicineDialog(QDialog):
    """
    Dialog for adding or editing medicine entries.
    
    Uses Ui_dlg_medicine_detail from Qt Designer for layout.
    
    Features:
    - Form validation
    - Auto ID generation (UUID)
    - Shelf dropdown populated from available shelves
    - Warning for past expiry dates
    - Image upload/remove
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
        self.selected_image_path: Optional[str] = None
        self.image_removed: bool = False
        
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        # Apply generated UI
        self.ui = Ui_dlg_medicine_detail()
        self.ui.setupUi(self)
        
        # Set window title based on mode
        title = "Sửa Thuốc" if self.is_edit_mode else "Thêm Thuốc Mới"
        self.setWindowTitle(title)
        self.ui.lbl_title.setText(title)
        
        # Populate shelf combo
        self.populate_shelves()
        
        # Connect buttons
        self.ui.btn_primary.clicked.connect(self.validate_and_save)
        self.ui.btn_secondary.clicked.connect(self.reject)
        
        # Image buttons
        self.ui.btn_add_img.clicked.connect(self.select_image)
        self.ui.btn_remove_img.clicked.connect(self.remove_image)
        self.ui.btn_remove_img.setEnabled(False)
        
        # Set button text based on mode
        self.ui.btn_primary.setText("Cập nhật" if self.is_edit_mode else "Save")
        
        # ID field: read-only in edit mode
        if self.is_edit_mode:
            self.ui.txt_medicine_id.setReadOnly(True)
    
    def populate_shelves(self):
        """Populate shelf dropdown with available shelves."""
        self.ui.cb_shelf_location.clear()
        
        if not self.shelves:
            self.ui.cb_shelf_location.addItem("Chưa có kệ nào", None)
            self.ui.cb_shelf_location.setEnabled(False)
            return
        
        self.ui.cb_shelf_location.addItem("Chọn kệ thuốc", None)
        for shelf in self.shelves:
            display_text = f"{shelf.id} - Khu {shelf.zone}, Cột {shelf.column}, Dãy {shelf.row}"
            self.ui.cb_shelf_location.addItem(display_text, shelf.id)
    
    def populate_fields(self):
        """Populate form fields with existing medicine data (Edit mode)."""
        if not self.medicine:
            return
        
        self.ui.txt_medicine_id.setText(self.medicine.id)
        self.ui.txt_medicine_name.setText(self.medicine.name)
        self.ui.txt_quantity.setText(str(self.medicine.quantity))
        
        # Set expiry date
        expiry_str = self.medicine.expiry_date.strftime("%d/%m/%Y")
        self.ui.txt_expiry_date.setText(expiry_str)
        
        self.ui.txt_price.setText(str(self.medicine.price))
        
        # Set shelf selection
        for i in range(self.ui.cb_shelf_location.count()):
            if self.ui.cb_shelf_location.itemData(i) == self.medicine.shelf_id:
                self.ui.cb_shelf_location.setCurrentIndex(i)
                break
        
        # Load existing image
        if self.medicine.image_path:
            abs_path = self.image_manager.get_image_path_from_relative(
                self.medicine.image_path
            )
            if abs_path:
                self._display_image(abs_path)
                self.ui.btn_remove_img.setEnabled(True)
    
    def validate_and_save(self):
        """Validate form input and save medicine."""
        # Validate name
        name = self.ui.txt_medicine_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên thuốc")
            self.ui.txt_medicine_name.setFocus()
            return
        
        # Validate quantity
        try:
            quantity = int(self.ui.txt_quantity.text().strip() or "0")
            if quantity < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số lượng phải là số nguyên không âm")
            self.ui.txt_quantity.setFocus()
            return
        
        # Validate price
        try:
            price = float(self.ui.txt_price.text().strip() or "0")
            if price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá phải là số không âm")
            self.ui.txt_price.setFocus()
            return
        
        # Validate shelf
        shelf_id = self.ui.cb_shelf_location.currentData()
        if shelf_id is None:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn kệ thuốc")
            return
        
        # Validate and parse expiry date
        expiry_text = self.ui.txt_expiry_date.text().strip()
        if not expiry_text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập hạn sử dụng")
            self.ui.txt_expiry_date.setFocus()
            return
        
        try:
            parts = expiry_text.split("/")
            if len(parts) == 3:
                expiry_date = date(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                raise ValueError
        except (ValueError, IndexError):
            QMessageBox.warning(
                self, "Lỗi", "Định dạng ngày không hợp lệ. Dùng dd/mm/yyyy"
            )
            self.ui.txt_expiry_date.setFocus()
            return
        
        # Warn if expiry date is in the past
        days_until_expiry = (expiry_date - date.today()).days
        if days_until_expiry < 0:
            reply = QMessageBox.warning(
                self, "Cảnh báo",
                f"Ngày hết hạn đã qua ({abs(days_until_expiry)} ngày). "
                "Bạn có chắc muốn tiếp tục?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        elif days_until_expiry < 30:
            reply = QMessageBox.warning(
                self, "Cảnh báo",
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
                self, "Xác nhận",
                f"Số lượng rất lớn ({quantity} đơn vị). "
                "Vui lòng xác nhận đây không phải lỗi nhập liệu.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                self.ui.txt_quantity.setFocus()
                return
        
        # Create medicine object
        try:
            if self.is_edit_mode:
                medicine_id = self.medicine.id
            else:
                medicine_id = ""
            
            # Determine image_path
            image_path = ""
            if self.selected_image_path:
                image_path = "__pending__"
            elif self.is_edit_mode and not self.image_removed:
                image_path = self.medicine.image_path if self.medicine.image_path else ""
            
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
            QMessageBox.warning(self, "Lỗi", f"Lỗi dữ liệu: {str(e)}")
    
    def get_medicine(self) -> Optional[Medicine]:
        """Get the created/edited medicine object."""
        return getattr(self, 'result_medicine', None)
    
    def get_selected_image_path(self) -> Optional[str]:
        """Get the path of the newly selected image."""
        return self.selected_image_path
    
    def is_image_removed(self) -> bool:
        """Check if user chose to remove the existing image."""
        return self.image_removed
    
    def select_image(self):
        """Open file dialog to select an image."""
        formats_filter = " ".join(f"*{fmt}" for fmt in SUPPORTED_FORMATS)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn ảnh thuốc", "",
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
        self.ui.btn_remove_img.setEnabled(True)
    
    def remove_image(self):
        """Remove the current image."""
        self.selected_image_path = None
        self.image_removed = True
        self.ui.lbl_upload_text.setText("Upload hình ảnh thuốc")
        self.ui.btn_remove_img.setEnabled(False)
    
    def _display_image(self, image_path: str):
        """Display an image in the upload frame."""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.ui.lbl_upload_text.setText("Không thể tải ảnh")
            return
        
        scaled = pixmap.scaled(
            280, 140,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.lbl_upload_text.setPixmap(scaled)
        self.ui.lbl_upload_text.setText("")
    
    def apply_theme(self):
        """Apply theme stylesheet to dialog."""
        pass  # Uses Qt Designer inline styles
