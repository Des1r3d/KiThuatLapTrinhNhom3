# Hệ Thống Quản Lý Kho Thuốc
"""
Hệ thống Quản lý Kho Thuốc - PHARMA.SYS

Các module:
- models: Model dữ liệu (Medicine, Shelf)
- storage: Thao tác file JSON
- inventory_manager: Thao tác CRUD
- alerts: Cảnh báo hết hạn và tồn kho
- search_engine: Tìm kiếm mờ
- dashboard_manager: Xử lý dữ liệu dashboard
"""

from src.models import Medicine, Shelf
from src.storage import StorageEngine
from src.inventory_manager import InventoryManager
from src.alerts import AlertSystem, AlertType, Alert
from src.search_engine import SearchEngine
from src.dashboard_manager import DashboardManager

__all__ = [
    'Medicine',
    'Shelf',
    'StorageEngine',
    'InventoryManager',
    'AlertSystem',
    'AlertType',
    'Alert',
    'SearchEngine',
    'DashboardManager',
]

