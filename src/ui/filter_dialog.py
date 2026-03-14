"""
Filter Medicine Dialog.

Uses Qt Designer-generated UI from loc_thuoc.py for layout.
Provides filtering options by shelf, price range, and status.
"""
from typing import Optional, List, Dict

from PyQt6.QtWidgets import QDialog

from src.models import Shelf
from src.ui.generated.loc_thuoc import Ui_dlg_filter_medicine


class FilterMedicineDialog(QDialog):
    """
    Dialog for filtering medicines by shelf, price, and status.
    
    Uses Ui_dlg_filter_medicine from Qt Designer for layout.
    """
    
    # Predefined price ranges
    PRICE_RANGES = [
        ("Tất cả", None, None),
        ("Dưới 10,000đ", 0, 10000),
        ("10,000đ - 50,000đ", 10000, 50000),
        ("50,000đ - 100,000đ", 50000, 100000),
        ("100,000đ - 500,000đ", 100000, 500000),
        ("Trên 500,000đ", 500000, None),
    ]
    
    # Status options
    STATUS_OPTIONS = [
        ("Tất cả", None),
        ("Bình thường", "normal"),
        ("Sắp hết hạn", "expiring"),
        ("Đã hết hạn", "expired"),
        ("Tồn kho thấp", "low_stock"),
        ("Hết hàng", "out_of_stock"),
    ]
    
    def __init__(
        self, parent=None,
        shelves: Optional[List[Shelf]] = None
    ):
        """
        Initialize Filter Medicine Dialog.
        
        Args:
            parent: Parent widget
            shelves: List of available shelves for filter options
        """
        super().__init__(parent)
        
        self.shelves = shelves or []
        self.result_filters: Optional[Dict] = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI using Qt Designer generated class."""
        self.ui = Ui_dlg_filter_medicine()
        self.ui.setupUi(self)
        
        # Populate shelf combo
        self.ui.cb_filter_shelf.clear()
        self.ui.cb_filter_shelf.addItem("Tất cả", None)
        for shelf in self.shelves:
            self.ui.cb_filter_shelf.addItem(shelf.id, shelf.id)
        
        # Populate price range combo
        self.ui.cb_filter_price.clear()
        for label, _, _ in self.PRICE_RANGES:
            self.ui.cb_filter_price.addItem(label)
        
        # Populate status combo
        self.ui.cb_filter_status.clear()
        for label, _ in self.STATUS_OPTIONS:
            self.ui.cb_filter_status.addItem(label)
        
        # Connect buttons
        self.ui.btn_primary.clicked.connect(self.apply_filters)
        self.ui.btn_secondary.clicked.connect(self.reject)
    
    def apply_filters(self):
        """Collect filter values and accept dialog."""
        # Get shelf filter
        shelf_id = self.ui.cb_filter_shelf.currentData()
        
        # Get price range
        price_idx = self.ui.cb_filter_price.currentIndex()
        if price_idx > 0 and price_idx < len(self.PRICE_RANGES):
            _, price_min, price_max = self.PRICE_RANGES[price_idx]
        else:
            price_min, price_max = None, None
        
        # Get status filter
        status_idx = self.ui.cb_filter_status.currentIndex()
        if status_idx > 0 and status_idx < len(self.STATUS_OPTIONS):
            _, status = self.STATUS_OPTIONS[status_idx]
        else:
            status = None
        
        self.result_filters = {
            'shelf_id': shelf_id,
            'price_min': price_min,
            'price_max': price_max,
            'status': status,
        }
        
        self.accept()
    
    def get_filters(self) -> Optional[Dict]:
        """
        Get the selected filter criteria.
        
        Returns:
            Dictionary with filter keys, or None if dialog was cancelled
        """
        return self.result_filters
