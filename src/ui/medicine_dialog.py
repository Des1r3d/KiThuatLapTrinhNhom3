"""
Medicine Dialog — PHARMA.SYS Add/Edit Medicine.

Uses Qt Designer-generated UI from them_thuoc.py for layout.
Features:
- Add mode: hides ID field (auto-generated), shows shelf selector
- Edit mode: shows ID (read-only), pre-fills all fields
- Input validation for all fields
- Image upload/remove
- Remaining shelf capacity display
- QDateEdit for expiry date selection
"""
from typing import Optional, List, Dict, Any
from datetime import date

from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIntValidator, QDoubleValidator

from src.models import Medicine, Shelf
from src.image_manager import ImageManager
from src.ui.theme import Theme
from src.ui.generated.them_thuoc import Ui_dlg_medicine_detail


class MedicineDialog(QDialog):
    """
    Dialog for adding or editing a medicine.

    Uses Ui_dlg_medicine_detail from them_thuoc.py for layout.
    
    Modes:
    - Add: Hides ID field, auto-generates ID on save
    - Edit: Shows ID (read-only), pre-fills data, validates changes

    Attributes:
        mode: 'add' or 'edit'
        medicine: Existing Medicine object (edit mode) or None (add mode)
        shelves: Available shelves for the shelf selector
        result_data: Validated data dictionary returned on accept
        selected_image_path: Path to selected image file
    """

    def __init__(
        self,
        parent=None,
        mode: str = "add",
        medicine: Optional[Medicine] = None,
        shelves: Optional[List[Shelf]] = None,
        image_manager: Optional[ImageManager] = None,
        theme: Optional[Theme] = None,
        remaining_capacity_func=None
    ):
        """
        Initialize Medicine Dialog.

        Args:
            parent: Parent widget
            mode: 'add' or 'edit'
            medicine: Medicine object to edit (edit mode only)
            shelves: List of Shelf objects for shelf selector
            image_manager: ImageManager for image operations
            theme: Theme instance for styling
            remaining_capacity_func: Callable(shelf_id, exclude_id) -> int
        """
        super().__init__(parent)

        self.mode = mode
        self.medicine = medicine
        self.shelves = shelves or []
        self.image_manager = image_manager or ImageManager()
        self.theme = theme or Theme()
        self.remaining_capacity_func = remaining_capacity_func
        self.result_data: Optional[Dict[str, Any]] = None
        self.selected_image_path: Optional[str] = None

        self.setup_ui()

        if mode == "edit" and medicine:
            self.load_medicine(medicine)

    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        self.ui = Ui_dlg_medicine_detail()
        self.ui.setupUi(self)

        # ── Mode-specific setup ──
        if self.mode == "add":
            self.setWindowTitle("Thêm thuốc mới")
            self.ui.lbl_title.setText("Thêm thuốc")
            # Hide ID field in Add mode (auto-generated)
            self.ui.lbl_id.setVisible(False)
            self.ui.txt_medicine_id.setVisible(False)
            self.ui.btn_primary.setText("Thêm")
            self.ui.btn_secondary.setText("Hủy")
        else:
            self.setWindowTitle("Chỉnh sửa thuốc")
            self.ui.lbl_title.setText("Chỉnh sửa thuốc")
            # Show ID (read-only) in Edit mode
            self.ui.txt_medicine_id.setReadOnly(True)
            self.ui.txt_medicine_id.setStyleSheet(
                self.ui.txt_medicine_id.styleSheet()
                + " color: #94A3B8;"
            )
            self.ui.btn_primary.setText("Lưu")
            self.ui.btn_secondary.setText("Hủy")

        # ── Populate shelf combo ──
        self.ui.cb_shelf_location.clear()
        self.ui.cb_shelf_location.addItem("Chọn kệ thuốc", None)
        for shelf in self.shelves:
            self.ui.cb_shelf_location.addItem(
                f"{shelf.id} (Còn chứa: {shelf.capacity})", shelf.id
            )

        # ── Input validators ──
        self.ui.txt_quantity.setValidator(QIntValidator(0, 999999, self))
        self.ui.txt_price.setValidator(QDoubleValidator(0, 999999999, 2, self))

        # ── Connect signals ──
        self.ui.btn_primary.clicked.connect(self.on_save)
        self.ui.btn_secondary.clicked.connect(self.reject)
        self.ui.btn_add_img.clicked.connect(self.on_add_image)
        self.ui.btn_remove_img.clicked.connect(self.on_remove_image)

        # Update remaining capacity when shelf changes
        self.ui.cb_shelf_location.currentIndexChanged.connect(
            self.update_remaining_capacity_display
        )

    def load_medicine(self, medicine: Medicine):
        """
        Pre-fill dialog fields with medicine data.

        Args:
            medicine: Medicine object to load
        """
        self.medicine = medicine

        # Fill fields
        self.ui.txt_medicine_id.setText(medicine.id)
        self.ui.txt_medicine_name.setText(medicine.name)
        self.ui.txt_quantity.setText(str(medicine.quantity))

        # Set expiry date
        qdate = QDate(
            medicine.expiry_date.year,
            medicine.expiry_date.month,
            medicine.expiry_date.day
        )
        self.ui.txt_expiry_date.setDate(qdate)

        # Set shelf selection
        for i in range(self.ui.cb_shelf_location.count()):
            if self.ui.cb_shelf_location.itemData(i) == medicine.shelf_id:
                self.ui.cb_shelf_location.setCurrentIndex(i)
                break

        # Price
        self.ui.txt_price.setText(str(medicine.price))

        # Load image if exists
        if medicine.image_path:
            abs_path = self.image_manager.get_image_path_from_relative(
                medicine.image_path
            )
            if abs_path:
                self._display_image(abs_path)

    def update_remaining_capacity_display(self):
        """Update shelf combo text to show remaining capacity."""
        if not self.remaining_capacity_func:
            return

        shelf_id = self.ui.cb_shelf_location.currentData()
        if shelf_id:
            exclude_id = self.medicine.id if self.medicine else ""
            remaining = self.remaining_capacity_func(shelf_id, exclude_id)
            # Update the placeholder text or a label to show remaining
            self.ui.lbl_shelf.setText(f"Kệ thuốc (Còn: {remaining} đơn vị)")
        else:
            self.ui.lbl_shelf.setText("Kệ thuốc")

    def on_save(self):
        """Validate inputs and accept dialog."""
        # ── Validation ──
        errors = []

        # Name
        name = self.ui.txt_medicine_name.text().strip()
        if not name:
            errors.append("Tên thuốc không được để trống")

        # Quantity
        qty_text = self.ui.txt_quantity.text().strip()
        if not qty_text:
            errors.append("Số lượng không được để trống")
        else:
            try:
                quantity = int(qty_text)
                if quantity < 0:
                    errors.append("Số lượng phải >= 0")
            except ValueError:
                errors.append("Số lượng phải là số nguyên")

        # Expiry Date
        qdate = self.ui.txt_expiry_date.date()
        expiry_date = date(qdate.year(), qdate.month(), qdate.day())

        # Shelf
        shelf_id = self.ui.cb_shelf_location.currentData()
        if not shelf_id:
            errors.append("Vui lòng chọn kệ thuốc")

        # Price
        price_text = self.ui.txt_price.text().strip()
        if not price_text:
            errors.append("Giá không được để trống")
        else:
            try:
                price = float(price_text)
                if price < 0:
                    errors.append("Giá phải >= 0")
            except ValueError:
                errors.append("Giá phải là số hợp lệ")

        # Show errors if any
        if errors:
            error_msg = "\n".join(f"• {e}" for e in errors)
            QMessageBox.warning(
                self,
                "Lỗi nhập liệu",
                f"Vui lòng sửa các lỗi sau:\n\n{error_msg}"
            )
            return

        # ── Build result data ──
        self.result_data = {
            "name": name,
            "quantity": int(qty_text),
            "expiry_date": expiry_date,
            "shelf_id": shelf_id,
            "price": float(price_text),
        }

        # Include image path if selected
        if self.selected_image_path:
            self.result_data["image_path"] = self.selected_image_path
        elif self.medicine and self.medicine.image_path:
            self.result_data["image_path"] = self.medicine.image_path

        self.accept()

    def on_add_image(self):
        """Handle image upload button click."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn hình ảnh thuốc",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if filepath:
            try:
                self.image_manager.validate_image(filepath)
                self.selected_image_path = filepath
                self._display_image(filepath)
            except (FileNotFoundError, ValueError) as e:
                QMessageBox.warning(
                    self, "Lỗi hình ảnh", str(e)
                )

    def on_remove_image(self):
        """Handle image remove button click."""
        self.selected_image_path = None
        self.ui.lbl_upload_text.setText("Upload hình ảnh thuốc")
        self.ui.lbl_upload_text.setPixmap(QPixmap())

    def _display_image(self, filepath: str):
        """
        Display image preview in the upload frame.

        Args:
            filepath: Absolute path to image file
        """
        pixmap = QPixmap(filepath)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                280, 140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.lbl_upload_text.setPixmap(scaled)
            self.ui.lbl_upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the validated form data.

        Returns:
            Dictionary with medicine field values, or None if cancelled
        """
        return self.result_data
