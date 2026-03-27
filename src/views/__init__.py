"""
Package views cho PHARMA.SYS.
Chứa các trang hiển thị chính của ứng dụng.
"""

from src.views.dashboard import Dashboard
from src.views.inventory_view import InventoryView
from src.views.shelf_view import ShelfView

__all__ = ['Dashboard', 'InventoryView', 'ShelfView']
