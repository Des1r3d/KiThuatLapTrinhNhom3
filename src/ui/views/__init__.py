"""
Package views cho PHARMA.SYS.
Chứa các trang hiển thị chính của ứng dụng.
"""

from src.ui.views.dashboard import Dashboard
from src.ui.views.inventory_view import InventoryView
from src.ui.views.shelf_view import ShelfView

__all__ = ['Dashboard', 'InventoryView', 'ShelfView']
