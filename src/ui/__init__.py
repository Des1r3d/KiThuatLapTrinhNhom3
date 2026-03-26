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

# Lazy imports to prevent circular dependency
_IMPORT_MAP = {
    'MainWindow': ('src.ui.main_window', 'MainWindow'),
    'InventoryView': ('src.views.inventory_view', 'InventoryView'),
    'MedicineDialog': ('src.dialogs.medicine_dialog', 'MedicineDialog'),
    'ShelfDialog': ('src.dialogs.shelf_dialog', 'ShelfDialog'),
    'MedicineDetailView': ('src.dialogs.medicine_detail_view', 'MedicineDetailView'),
    'FilterMedicineDialog': ('src.dialogs.filter_dialog', 'FilterMedicineDialog'),
    'Dashboard': ('src.views.dashboard', 'Dashboard'),
    'Theme': ('src.ui.theme', 'Theme'),
    'ThemeMode': ('src.ui.theme', 'ThemeMode'),
    'AddSuccessDialog': ('src.dialogs.notification_dialogs', 'AddSuccessDialog'),
    'EditSuccessDialog': ('src.dialogs.notification_dialogs', 'EditSuccessDialog'),
    'DeleteSuccessDialog': ('src.dialogs.notification_dialogs', 'DeleteSuccessDialog'),
    'ConfirmDeleteDialog': ('src.dialogs.notification_dialogs', 'ConfirmDeleteDialog'),
    'ShelfFullErrorDialog': ('src.dialogs.notification_dialogs', 'ShelfFullErrorDialog'),
}


def __getattr__(name):
    if name in _IMPORT_MAP:
        module_path, attr_name = _IMPORT_MAP[name]
        import importlib
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
