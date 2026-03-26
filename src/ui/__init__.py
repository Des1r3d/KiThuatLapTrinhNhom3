"""
Package UI cho Hệ Thống Quản Lý Kho Thuốc.

Package này chứa tất cả thành phần giao diện PyQt6:
- MainWindow: Cửa sổ ứng dụng chính
- InventoryView: Bảng danh sách thuốc
- MedicineDialog: Hộp thoại Thêm/Sửa thuốc
- ShelfDialog: Hộp thoại Thêm/Sửa kệ
- MedicineDetailView: Xem chi tiết thuốc (chỉ đọc)
- FilterMedicineDialog: Hộp thoại lọc thuốc
- Dashboard: Thống kê và biểu đồ
- Theme: Hệ thống màu và kiểu dáng
- Hộp thoại thông báo: Thành công/Lỗi/Xác nhận
"""

from src.ui.main_window import MainWindow
from src.views.inventory_view import InventoryView
from src.dialogs.medicine_dialog import MedicineDialog
from src.dialogs.shelf_dialog import ShelfDialog
from src.dialogs.medicine_detail_view import MedicineDetailView
from src.dialogs.filter_dialog import FilterMedicineDialog
from src.views.dashboard import Dashboard
from src.ui.theme import Theme, ThemeMode
from src.dialogs.notification_dialogs import (
    AddSuccessDialog, EditSuccessDialog, DeleteSuccessDialog,
    ConfirmDeleteDialog, ShelfFullErrorDialog
)

__all__ = [
    'MainWindow',
    'InventoryView',
    'MedicineDialog',
    'ShelfDialog',
    'MedicineDetailView',
    'FilterMedicineDialog',
    'Dashboard',
    'Theme',
    'ThemeMode',
    'AddSuccessDialog',
    'EditSuccessDialog',
    'DeleteSuccessDialog',
    'ConfirmDeleteDialog',
    'ShelfFullErrorDialog',
]
