"""
Inventory View — PHARMA.SYS Medicine Table.

Uses Qt Designer-generated UI from inventory_view_ui.py for layout.
Features:
- Sortable table with color-coded status badges (pill shape)
- Context menu (Edit/Delete)
- Double-click to edit
- Alternating row colors with colored text for alert statuses
"""
from typing import List, Optional
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QMenu, QHeaderView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QAction

from src.models import Medicine
from src.ui.theme import Theme
from src.ui.generated.inventory_view_ui import Ui_InventoryView


class InventoryView(QWidget):
    """
    Widget for displaying medicines in a table.

    Uses Ui_InventoryView from inventory_view_ui.py for layout.

    Features:
    - Status badges (pill shape) with color coding
    - Sortable columns
    - Context menu for Edit/Delete
    - Double-click to edit
    - Real-time status indicators

    Signals:
        medicine_selected: Emitted when a medicine is double-clicked
        edit_requested: Emitted when edit is requested (medicine_id)
        delete_requested: Emitted when delete is requested (medicine_id)
    """

    medicine_selected = pyqtSignal(str)  # medicine_id
    add_requested = pyqtSignal()         # request to add a new medicine
    edit_requested = pyqtSignal(str)     # medicine_id
    delete_requested = pyqtSignal(str)   # medicine_id
    detail_requested = pyqtSignal(str)   # medicine_id
    filter_requested = pyqtSignal()      # request to show filter dialog

    def __init__(self, parent=None, theme: Optional[Theme] = None):
        """
        Initialize Inventory View.

        Args:
            parent: Parent widget
            theme: Theme instance for styling
        """
        super().__init__(parent)

        self.theme = theme or Theme()
        self.medicines: List[Medicine] = []
        self.filtered_medicines: List[Medicine] = []
        self.active_filters: Optional[dict] = None

        self.setup_ui()

    def setup_ui(self):
        """Setup table UI using Qt Designer generated class."""
        self.ui = Ui_InventoryView()
        self.ui.setupUi(self)

        # Configure column widths (not in .ui)
        header = self.ui.tbl_medicines.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        # Row height
        self.ui.tbl_medicines.verticalHeader().setDefaultSectionSize(42)

        # Connect signals
        self.ui.btn_add.clicked.connect(lambda: self.add_requested.emit())
        self.ui.btn_filter.clicked.connect(lambda: self.filter_requested.emit())
        self.ui.btn_clear_filter.clicked.connect(self.clear_filters)
        self.ui.tbl_medicines.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.ui.tbl_medicines.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.tbl_medicines.customContextMenuRequested.connect(
            self.show_context_menu
        )

    def load_medicines(self, medicines: List[Medicine]):
        """
        Load medicines into table.

        Args:
            medicines: List of Medicine objects to display
        """
        self.medicines = medicines
        self.apply_current_filters()

    def apply_current_filters(self):
        """Apply current active filters and refresh table."""
        if self.active_filters:
            self.filtered_medicines = self.filter_medicines(
                self.medicines, self.active_filters
            )
        else:
            self.filtered_medicines = list(self.medicines)

        self.ui.tbl_medicines.setSortingEnabled(False)  # Disable during update
        self.ui.tbl_medicines.setRowCount(0)

        for medicine in self.filtered_medicines:
            self.add_medicine_row(medicine)

        self.ui.tbl_medicines.setSortingEnabled(True)
        self.update_count_label()

    def add_medicine_row(self, medicine: Medicine):
        """
        Add a single medicine row to table.

        Args:
            medicine: Medicine object to add
        """
        row = self.ui.tbl_medicines.rowCount()
        self.ui.tbl_medicines.insertRow(row)

        # ID
        id_item = QTableWidgetItem(medicine.id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tbl_medicines.setItem(row, 0, id_item)

        # Name
        name_item = QTableWidgetItem(medicine.name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        name_font = name_item.font()
        name_font.setWeight(QFont.Weight.Medium)
        name_item.setFont(name_font)
        self.ui.tbl_medicines.setItem(row, 1, name_item)

        # Quantity
        quantity_item = QTableWidgetItem(str(medicine.quantity))
        quantity_item.setData(Qt.ItemDataRole.UserRole, medicine.quantity)
        quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_medicines.setItem(row, 2, quantity_item)

        # Expiry Date
        expiry_str = medicine.expiry_date.strftime("%d/%m/%Y")
        expiry_item = QTableWidgetItem(expiry_str)
        expiry_item.setData(
            Qt.ItemDataRole.UserRole,
            medicine.expiry_date.toordinal()
        )
        expiry_item.setFlags(expiry_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tbl_medicines.setItem(row, 3, expiry_item)

        # Shelf
        shelf_item = QTableWidgetItem(medicine.shelf_id)
        shelf_item.setFlags(shelf_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        shelf_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_medicines.setItem(row, 4, shelf_item)

        # Price
        price_str = f"{medicine.price:,.2f}"
        price_item = QTableWidgetItem(price_str)
        price_item.setData(Qt.ItemDataRole.UserRole, medicine.price)
        price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tbl_medicines.setItem(row, 5, price_item)

        # Status — badge style
        status_text, status_type = self.get_medicine_status(medicine)
        status_item = QTableWidgetItem(status_text)
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Apply badge colors
        if status_type != "normal":
            alert_colors = self.theme.get_alert_colors(status_type)
        else:
            alert_colors = self.theme.get_alert_colors('success')

        status_item.setBackground(QColor(alert_colors['bg']))
        status_item.setForeground(QColor(alert_colors['text']))
        status_font = status_item.font()
        status_font.setBold(True)
        status_font.setPointSize(Theme.FONT_SIZE_BADGE)
        status_item.setFont(status_font)

        self.ui.tbl_medicines.setItem(row, 6, status_item)

        # Apply row coloring based on status
        self.apply_row_color(row, status_type, medicine)

    def get_medicine_status(self, medicine: Medicine) -> tuple[str, str]:
        """
        Get status text and type for a medicine.

        Args:
            medicine: Medicine object

        Returns:
            Tuple of (status_text, status_type)
            status_type: 'danger', 'warning', 'low_stock', or 'normal'
        """
        # Check if expired
        if medicine.is_expired():
            days_overdue = abs(medicine.days_until_expiry())
            return f"Hết hạn ({days_overdue} ngày)", "danger"

        # Check if out of stock
        if medicine.quantity == 0:
            return "Hết hàng", "danger"

        # Check if expiring soon
        days_left = medicine.days_until_expiry()
        if days_left <= 30:
            return f"Sắp hết hạn ({days_left} ngày)", "warning"

        # Check if low stock
        if medicine.quantity <= 5:
            return "Tồn kho thấp", "low_stock"

        return "Còn hàng", "normal"

    def apply_row_color(self, row: int, status_type: str, medicine: Medicine):
        """
        Apply colored text to entire row based on status.
        Row background remains alternating (handled by Qt); only foreground changes.

        Args:
            row: Row index
            status_type: Status type ('danger', 'warning', 'low_stock', 'normal')
            medicine: Medicine object
        """
        if status_type == "normal":
            return

        alert_colors = self.theme.get_alert_colors(status_type)
        text_color = QColor(alert_colors['text'])

        for col in range(self.ui.tbl_medicines.columnCount() - 1):  # Skip status column
            item = self.ui.tbl_medicines.item(row, col)
            if item:
                item.setForeground(text_color)

    def on_item_double_clicked(self, item: QTableWidgetItem):
        """Handle double-click on table item — show detail view."""
        row = item.row()
        medicine_id = self.ui.tbl_medicines.item(row, 0).text()
        self.detail_requested.emit(medicine_id)

    def show_context_menu(self, position):
        """
        Show context menu for table row.

        Args:
            position: Position where menu was requested
        """
        item = self.ui.tbl_medicines.itemAt(position)
        if not item:
            return

        row = item.row()
        medicine_id = self.ui.tbl_medicines.item(row, 0).text()
        medicine_name = self.ui.tbl_medicines.item(row, 1).text()

        menu = QMenu(self)

        # Edit action
        edit_action = QAction("Chỉnh sửa thuốc", self)
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(medicine_id)
        )
        menu.addAction(edit_action)

        # Delete action
        delete_action = QAction("Xóa thuốc", self)
        delete_action.triggered.connect(
            lambda: self.confirm_delete(medicine_id, medicine_name)
        )
        menu.addAction(delete_action)

        menu.exec(self.ui.tbl_medicines.viewport().mapToGlobal(position))

    def confirm_delete(self, medicine_id: str, medicine_name: str):
        """
        Phát tín hiệu xóa — hộp thoại xác nhận thực sự được hiển thị
        bởi main_window.delete_medicine() (ConfirmDeleteDialog).

        Args:
            medicine_id: ID thuốc cần xóa
            medicine_name: Tên thuốc (không dùng ở đây, giữ lại chữ ký)
        """
        self.delete_requested.emit(medicine_id)

    def update_count_label(self):
        """Update the count label with current medicine count."""
        total = len(self.medicines)
        shown = len(self.filtered_medicines)
        if self.active_filters:
            self.ui.lbl_count.setText(f"{shown}/{total} mục (đã lọc)")
        else:
            self.ui.lbl_count.setText(f"{total} mục")

    def refresh(self):
        """Refresh the table display."""
        self.apply_current_filters()

    def set_filters(self, filters: Optional[dict]):
        """
        Set active filters and refresh display.

        Args:
            filters: Dictionary with filter criteria, or None to clear
        """
        self.active_filters = filters
        if filters:
            self.ui.btn_clear_filter.setVisible(True)
            self.ui.btn_filter.setText("Đã lọc")
        else:
            self.ui.btn_clear_filter.setVisible(False)
            self.ui.btn_filter.setText("Lọc")
        self.apply_current_filters()

    def clear_filters(self):
        """Clear all active filters."""
        self.set_filters(None)

    @staticmethod
    def filter_medicines(medicines: List[Medicine], filters: dict) -> List[Medicine]:
        """
        Filter medicines by given criteria.

        Args:
            medicines: List of medicines to filter
            filters: Dictionary with keys: shelf_id, price_min, price_max, status

        Returns:
            Filtered list of medicines
        """
        result = list(medicines)

        # Filter by shelf
        shelf_id = filters.get('shelf_id')
        if shelf_id:
            result = [m for m in result if m.shelf_id == shelf_id]

        # Filter by price range
        price_min = filters.get('price_min')
        price_max = filters.get('price_max')
        if price_min is not None:
            result = [m for m in result if m.price >= price_min]
        if price_max is not None:
            result = [m for m in result if m.price <= price_max]

        # Filter by status
        status = filters.get('status')
        if status:
            filtered_by_status = []
            for m in result:
                if status == 'expired' and m.is_expired():
                    filtered_by_status.append(m)
                elif status == 'expiring' and not m.is_expired() and m.days_until_expiry() <= 30:
                    filtered_by_status.append(m)
                elif status == 'low_stock' and 0 < m.quantity <= 5:
                    filtered_by_status.append(m)
                elif status == 'out_of_stock' and m.quantity == 0:
                    filtered_by_status.append(m)
                elif status == 'normal' and not m.is_expired() and m.days_until_expiry() > 30 and m.quantity > 5:
                    filtered_by_status.append(m)
            result = filtered_by_status

        return result

    def apply_theme(self):
        """Apply theme stylesheet."""
        pass  # Uses global theme from MainWindow

    def get_selected_medicine_id(self) -> Optional[str]:
        """
        Get ID of currently selected medicine.

        Returns:
            Medicine ID if a row is selected, None otherwise
        """
        current_row = self.ui.tbl_medicines.currentRow()
        if current_row >= 0:
            return self.ui.tbl_medicines.item(current_row, 0).text()
        return None
