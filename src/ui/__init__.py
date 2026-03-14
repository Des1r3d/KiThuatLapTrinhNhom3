"""
UI package for Pharmacy Management System.

This package contains all PyQt6 UI components:
- MainWindow: Main application window
- InventoryView: Medicine table view
- MedicineDialog: Add/Edit medicine dialog
- Dashboard: Statistics and charts
- Theme: Color system and styling
"""

from src.ui.main_window import MainWindow
from src.ui.inventory_view import InventoryView
from src.ui.medicine_dialog import MedicineDialog
from src.ui.dashboard import Dashboard
from src.ui.theme import Theme, ThemeMode

__all__ = [
    'MainWindow',
    'InventoryView',
    'MedicineDialog',
    'Dashboard',
    'Theme',
    'ThemeMode'
]
