"""
Medicine Detail View dialog.

Uses Qt Designer-generated UI from thong_tin_thuoc.py for layout.
Displays read-only medicine information with image, basic info,
stock info, and price sections.
"""
from typing import Optional

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from src.models import Medicine
from src.image_manager import ImageManager
from src.ui.generated.thong_tin_thuoc import Ui_dlg_medicine_detail


class MedicineDetailView(QDialog):
    """
    Read-only dialog for viewing medicine details.
    
    Uses Ui_dlg_medicine_detail from thong_tin_thuoc.py for layout.
    
    Signals:
        edit_requested: Emitted when 'Chỉnh sửa' button is clicked (medicine_id)
        delete_requested: Emitted when 'Xóa thuốc' button is clicked (medicine_id)
    """
    
    edit_requested = pyqtSignal(str)    # medicine_id
    delete_requested = pyqtSignal(str)  # medicine_id
    
    def __init__(
        self, parent=None,
        medicine: Optional[Medicine] = None,
        image_manager: Optional[ImageManager] = None
    ):
        """
        Initialize Medicine Detail View.
        
        Args:
            parent: Parent widget
            medicine: Medicine object to display
            image_manager: ImageManager for loading images
        """
        super().__init__(parent)
        
        self.medicine = medicine
        self.image_manager = image_manager or ImageManager()
        
        self.setup_ui()
        
        if medicine:
            self.load_medicine(medicine)
    
    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        self.ui = Ui_dlg_medicine_detail()
        self.ui.setupUi(self)
        
        # Connect buttons
        self.ui.btn_primary.clicked.connect(self._on_edit_clicked)
        self.ui.btn_secondary.clicked.connect(self._on_delete_clicked)
    
    def load_medicine(self, medicine: Medicine):
        """
        Populate dialog with medicine data.
        
        Args:
            medicine: Medicine object to display
        """
        self.medicine = medicine
        
        # Name and status
        self.ui.lbl_detail_name.setText(medicine.name)
        
        # Status tag
        if medicine.is_expired():
            self.ui.lbl_status_tag.setText("Hết hạn")
            self.ui.lbl_status_tag.setStyleSheet(
                "background-color: #FEE2E2; color: #EF4444; "
                "padding: 4px 8px; border-radius: 10px; "
                "font-size: 12px; font-weight: bold;"
            )
        elif medicine.days_until_expiry() <= 30:
            self.ui.lbl_status_tag.setText("Sắp hết hạn")
            self.ui.lbl_status_tag.setStyleSheet(
                "background-color: #FEF3C7; color: #D97706; "
                "padding: 4px 8px; border-radius: 10px; "
                "font-size: 12px; font-weight: bold;"
            )
        elif medicine.quantity == 0:
            self.ui.lbl_status_tag.setText("Hết hàng")
            self.ui.lbl_status_tag.setStyleSheet(
                "background-color: #FEE2E2; color: #EF4444; "
                "padding: 4px 8px; border-radius: 10px; "
                "font-size: 12px; font-weight: bold;"
            )
        elif medicine.quantity <= 5:
            self.ui.lbl_status_tag.setText("Tồn kho thấp")
            self.ui.lbl_status_tag.setStyleSheet(
                "background-color: #FEF3C7; color: #B45309; "
                "padding: 4px 8px; border-radius: 10px; "
                "font-size: 12px; font-weight: bold;"
            )
        else:
            self.ui.lbl_status_tag.setText("Bình thường")
            self.ui.lbl_status_tag.setStyleSheet(
                "background-color: #D1FAE5; color: #059669; "
                "padding: 4px 8px; border-radius: 10px; "
                "font-size: 12px; font-weight: bold;"
            )
        
        # Basic info
        self.ui.lbl_data_generic_name.setText(medicine.name)
        self.ui.lbl_data_expiry.setText(
            medicine.expiry_date.strftime("%d/%m/%Y")
        )
        
        # Stock info
        self.ui.lbl_data_quantity.setText(f"{medicine.quantity} (Đơn vị)")
        self.ui.lbl_data_shelf.setText(medicine.shelf_id)
        
        # Price
        self.ui.lbl_data_price.setText(f"{medicine.price:,.0f}đ")
        
        # Load image
        if medicine.image_path:
            abs_path = self.image_manager.get_image_path_from_relative(
                medicine.image_path
            )
            if abs_path:
                pixmap = QPixmap(abs_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(
                        280, 280,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.ui.lbl_medicine_image.setPixmap(scaled)
                    self.ui.lbl_medicine_image.setText("")
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        if self.medicine:
            self.edit_requested.emit(self.medicine.id)
            self.accept()
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        if self.medicine:
            self.delete_requested.emit(self.medicine.id)
            self.accept()
