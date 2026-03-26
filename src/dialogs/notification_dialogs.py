"""
Notification dialogs for success/error/confirmation messages.

Uses Qt Designer-generated UI classes for layout:
- AddSuccessDialog: them_thanh_cong.py / them_thanh_cong_dark.py
- EditSuccessDialog: sua_thanh_cong.py / sua_thanh_cong_dark.py
- DeleteSuccessDialog: xoa_thanh_cong.py / xoa_thanh_cong_dark.py
- ConfirmDeleteDialog: xac_nhan_xoa.py / xac_nhan_xoa_dark.py
- ShelfFullErrorDialog: ke_day.py

Each dialog selects the light or dark UI variant based on the
current ThemeMode passed in via the `theme` parameter.
"""
from typing import Optional

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from src.ui.theme import Theme, ThemeMode

# Light UI classes
from src.ui.generated.them_thanh_cong import Ui_dlg_add_success
from src.ui.generated.sua_thanh_cong import Ui_dlg_edit_success
from src.ui.generated.xoa_thanh_cong import Ui_dlg_success
from src.ui.generated.xac_nhan_xoa import Ui_dlg_confirm_delete
from src.ui.generated.ke_day import Ui_dlg_error_full

# Dark UI classes
from src.ui.generated.them_thanh_cong_dark import Ui_dlg_add_success as Ui_dlg_add_success_dark
from src.ui.generated.sua_thanh_cong_dark import Ui_dlg_edit_success as Ui_dlg_edit_success_dark
from src.ui.generated.xoa_thanh_cong_dark import Ui_dlg_success as Ui_dlg_success_dark
from src.ui.generated.xac_nhan_xoa_dark import Ui_dlg_confirm_delete as Ui_dlg_confirm_delete_dark


class AddSuccessDialog(QDialog):
    """Notification dialog shown after successfully adding a medicine."""
    
    def __init__(self, parent=None, medicine_name: str = "", medicine_id: str = "", theme: Optional[Theme] = None):
        super().__init__(parent)
        self.theme = theme or Theme()
        
        # Choose UI class based on theme mode
        if self.theme.mode == ThemeMode.DARK:
            self.ui = Ui_dlg_add_success_dark()
        else:
            self.ui = Ui_dlg_add_success()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Thêm thuốc thành công")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Update dynamic content
        self.ui.lbl_desc.setText(
            f"Thuốc '{medicine_name}' đã được thêm vào kho hệ thống"
        )
        self.ui.lbl_code.setText(f"Mã thuốc: {medicine_id}")
        
        # Connect close button
        self.ui.btn_close.clicked.connect(self.accept)


class EditSuccessDialog(QDialog):
    """Notification dialog shown after successfully editing a medicine."""
    
    def __init__(self, parent=None, medicine_name: str = "", medicine_id: str = "", theme: Optional[Theme] = None):
        super().__init__(parent)
        self.theme = theme or Theme()
        
        # Choose UI class based on theme mode
        if self.theme.mode == ThemeMode.DARK:
            self.ui = Ui_dlg_edit_success_dark()
        else:
            self.ui = Ui_dlg_edit_success()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Sửa thuốc thành công")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Update dynamic content
        self.ui.lbl_desc.setText(
            f"Thông tin thuốc '{medicine_name}' đã được cập nhật"
        )
        self.ui.lbl_code.setText(f"Mã thuốc: {medicine_id}")
        
        # Connect close button
        self.ui.btn_close.clicked.connect(self.accept)


class DeleteSuccessDialog(QDialog):
    """Notification dialog shown after successfully deleting a medicine."""
    
    def __init__(self, parent=None, medicine_name: str = "", medicine_id: str = "", theme: Optional[Theme] = None):
        super().__init__(parent)
        self.theme = theme or Theme()
        
        # Choose UI class based on theme mode
        if self.theme.mode == ThemeMode.DARK:
            self.ui = Ui_dlg_success_dark()
        else:
            self.ui = Ui_dlg_success()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Xóa thuốc thành công")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Update dynamic content
        # Note: xoa_thanh_cong.ui does not have lbl_desc — use lbl_code instead
        self.ui.lbl_code.setText(
            f"Thuốc '{medicine_name}' | Mã: {medicine_id}"
        )
        
        # Connect close button
        self.ui.btn_close.clicked.connect(self.accept)


class ConfirmDeleteDialog(QDialog):
    """
    Confirmation dialog before deleting a medicine.
    
    Has two buttons:
    - btn_delete: confirm delete (returns Accepted)
    - btn_cancel: cancel (returns Rejected)
    """
    
    def __init__(
        self, parent=None,
        medicine_name: str = "",
        medicine_id: str = "",
        quantity: int = 0,
        theme: Optional[Theme] = None
    ):
        super().__init__(parent)
        self.theme = theme or Theme()
        
        # Choose UI class based on theme mode
        if self.theme.mode == ThemeMode.DARK:
            self.ui = Ui_dlg_confirm_delete_dark()
        else:
            self.ui = Ui_dlg_confirm_delete()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Xác nhận xóa")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Update dynamic content
        self.ui.lbl_qty.setText(f"SỐ LƯỢNG: {quantity}")
        self.ui.lbl_code.setText(f"Mã thuốc: {medicine_id}")
        
        if quantity > 0:
            self.ui.lbl_warning.setText("CẢNH BÁO: VẪN CÒN TỒN KHO")
            self.ui.lbl_warning.setVisible(True)
        else:
            self.ui.lbl_warning.setVisible(False)
        
        # Connect buttons
        self.ui.btn_delete.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)


class ShelfFullErrorDialog(QDialog):
    """Error dialog shown when a shelf is full and cannot accept more medicines."""
    
    def __init__(
        self, parent=None,
        shelf_id: str = "",
        remaining_capacity: int = 0,
        theme: Optional[Theme] = None
    ):
        super().__init__(parent)
        self.theme = theme or Theme()
        self.ui = Ui_dlg_error_full()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Lỗi - Kệ đầy")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Update dynamic content
        self.ui.lbl_desc.setText(
            f"Kệ {shelf_id} hiện tại chỉ còn sức chứa "
            f"{remaining_capacity} đơn vị thuốc. "
            "Vui lòng chọn kệ khác hoặc thay đổi lượng thuốc nhập vào"
        )
        
        # Connect close button
        self.ui.btn_close.clicked.connect(self.accept)
