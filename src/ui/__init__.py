"""
UI package for Pharmacy Management System.

This package contains all PyQt6 UI components:
- MainWindow: Main application window
- InventoryView: Medicine table view
- MedicineDialog: Add/Edit medicine dialog
- ShelfDialog: Add/Edit shelf dialog
- MedicineDetailView: Read-only medicine detail view
- FilterMedicineDialog: Medicine filter dialog
- Dashboard: Statistics and charts
- Theme: Color system and styling
- Notification dialogs: Success/Error/Confirm dialogs
"""

from src.ui.main_window import MainWindow
from src.ui.inventory_view import InventoryView
from src.ui.medicine_dialog import MedicineDialog
from src.ui.shelf_dialog import ShelfDialog
from src.ui.medicine_detail_view import MedicineDetailView
from src.ui.filter_dialog import FilterMedicineDialog
from src.ui.dashboard import Dashboard
from src.ui.theme import Theme, ThemeMode
from src.ui.notification_dialogs import (
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
