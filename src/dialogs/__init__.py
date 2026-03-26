"""
Package hộp thoại cho PHARMA.SYS.
Chứa các cửa sổ hộp thoại để tạo, chỉnh sửa, xem chi tiết và thông báo.
"""

from src.dialogs.medicine_dialog import MedicineDialog
from src.dialogs.shelf_dialog import ShelfDialog
from src.dialogs.filter_dialog import FilterMedicineDialog
from src.dialogs.medicine_detail_view import MedicineDetailView
from src.dialogs.notification_dialogs import (
    AddSuccessDialog, EditSuccessDialog, DeleteSuccessDialog,
    ConfirmDeleteDialog, ShelfFullErrorDialog
)

__all__ = [
    'MedicineDialog',
    'ShelfDialog',
    'FilterMedicineDialog',
    'MedicineDetailView',
    'AddSuccessDialog',
    'EditSuccessDialog',
    'DeleteSuccessDialog',
    'ConfirmDeleteDialog',
    'ShelfFullErrorDialog',
]
