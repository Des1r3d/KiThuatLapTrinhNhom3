"""
Inventory View - Table display for medicines.

Features:
- Sortable table with color-coded status
- Context menu (Edit/Delete)
- Double-click to edit
- Alert highlighting (Expired, Expiring Soon, Low Stock)
"""
from typing import List, Optional
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMenu,
    QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QAction

from src.models import Medicine
from src.ui.theme import Theme


class InventoryView(QWidget):
    """
    Widget for displaying medicines in a table.
    
    Features:
    - Color-coded rows based on medicine status
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
    edit_requested = pyqtSignal(str)     # medicine_id
    delete_requested = pyqtSignal(str)   # medicine_id
    
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
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup table UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Danh Sách Thuốc")
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H2)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Count label
        self.count_label = QLabel("0 thuốc")
        self.count_label.setProperty("secondary", True)
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên thuốc", "Số lượng", "Hạn dùng", 
            "Kệ", "Giá (VNĐ)", "Trạng thái"
        ])
        
        # Table properties
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        # Connect signals
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table.customContextMenuRequested.connect(
            self.show_context_menu
        )
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_medicines(self, medicines: List[Medicine]):
        """
        Load medicines into table.
        
        Args:
            medicines: List of Medicine objects to display
        """
        self.medicines = medicines
        self.table.setSortingEnabled(False)  # Disable during update
        self.table.setRowCount(0)
        
        for medicine in medicines:
            self.add_medicine_row(medicine)
        
        self.table.setSortingEnabled(True)
        self.update_count_label()
    
    def add_medicine_row(self, medicine: Medicine):
        """
        Add a single medicine row to table.
        
        Args:
            medicine: Medicine object to add
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # ID
        id_item = QTableWidgetItem(medicine.id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 0, id_item)
        
        # Name
        name_item = QTableWidgetItem(medicine.name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 1, name_item)
        
        # Quantity
        quantity_item = QTableWidgetItem(str(medicine.quantity))
        quantity_item.setData(Qt.ItemDataRole.UserRole, medicine.quantity)
        quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 2, quantity_item)
        
        # Expiry Date
        expiry_str = medicine.expiry_date.strftime("%d/%m/%Y")
        expiry_item = QTableWidgetItem(expiry_str)
        expiry_item.setData(
            Qt.ItemDataRole.UserRole, 
            medicine.expiry_date.toordinal()
        )
        expiry_item.setFlags(expiry_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 3, expiry_item)
        
        # Shelf
        shelf_item = QTableWidgetItem(medicine.shelf_id)
        shelf_item.setFlags(shelf_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 4, shelf_item)
        
        # Price
        price_str = f"{medicine.price:,.2f}"
        price_item = QTableWidgetItem(price_str)
        price_item.setData(Qt.ItemDataRole.UserRole, medicine.price)
        price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 5, price_item)
        
        # Status
        status_text, status_type = self.get_medicine_status(medicine)
        status_item = QTableWidgetItem(status_text)
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 6, status_item)
        
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
            return f"Hết hạn ({days_overdue}d)", "danger"
        
        # Check if out of stock
        if medicine.quantity == 0:
            return "Hết hàng", "danger"
        
        # Check if expiring soon
        days_left = medicine.days_until_expiry()
        if days_left <= 30:
            return f"Sắp hết hạn ({days_left}d)", "warning"
        
        # Check if low stock
        if medicine.quantity <= 5:
            return f"Tồn kho thấp", "low_stock"
        
        return "Bình thường", "normal"
    
    def apply_row_color(self, row: int, status_type: str, medicine: Medicine):
        """
        Apply background color to row based on status.
        
        Args:
            row: Row index
            status_type: Status type ('danger', 'warning', 'low_stock', 'normal')
            medicine: Medicine object
        """
        if status_type == "normal":
            return
        
        alert_colors = self.theme.get_alert_colors(status_type)
        bg_color = QColor(alert_colors['bg'])
        text_color = QColor(alert_colors['text'])
        
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setBackground(bg_color)
                # Make expiry date and quantity columns have alert text color
                if col in [2, 3, 6]:  # Quantity, Expiry, Status columns
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    item.setForeground(text_color)
    
    def on_item_double_clicked(self, item: QTableWidgetItem):
        """Handle double-click on table item."""
        row = item.row()
        medicine_id = self.table.item(row, 0).text()
        self.edit_requested.emit(medicine_id)
    
    def show_context_menu(self, position):
        """
        Show context menu for table row.
        
        Args:
            position: Position where menu was requested
        """
        item = self.table.itemAt(position)
        if not item:
            return
        
        row = item.row()
        medicine_id = self.table.item(row, 0).text()
        medicine_name = self.table.item(row, 1).text()
        
        menu = QMenu(self)
        
        # Edit action
        edit_action = QAction("✏️ Sửa thuốc", self)
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(medicine_id)
        )
        menu.addAction(edit_action)
        
        # Delete action
        delete_action = QAction("🗑️ Xóa thuốc", self)
        delete_action.triggered.connect(
            lambda: self.confirm_delete(medicine_id, medicine_name)
        )
        menu.addAction(delete_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def confirm_delete(self, medicine_id: str, medicine_name: str):
        """
        Show confirmation dialog before deleting.
        
        Args:
            medicine_id: ID of medicine to delete
            medicine_name: Name of medicine for confirmation message
        """
        # Find medicine to check quantity
        medicine = next(
            (m for m in self.medicines if m.id == medicine_id), 
            None
        )
        
        if medicine and medicine.quantity > 0:
            # Strong confirmation for medicines with stock
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                f"Bạn có chắc chắn muốn xóa thuốc '{medicine_name}' "
                f"hiện đang còn {medicine.quantity} đơn vị trong kho?\n\n"
                "Thao tác này không thể hoàn tác.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
        else:
            # Regular confirmation
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                f"Bạn có chắc chắn muốn xóa thuốc '{medicine_name}'?\n\n"
                "Thao tác này không thể hoàn tác.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(medicine_id)
    
    def update_count_label(self):
        """Update the count label with current medicine count."""
        count = len(self.medicines)
        self.count_label.setText(f"{count} thuốc")
    
    def refresh(self):
        """Refresh the table display."""
        self.load_medicines(self.medicines)
    
    def apply_theme(self):
        """Apply theme stylesheet."""
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def get_selected_medicine_id(self) -> Optional[str]:
        """
        Get ID of currently selected medicine.
        
        Returns:
            Medicine ID if a row is selected, None otherwise
        """
        current_row = self.table.currentRow()
        if current_row >= 0:
            return self.table.item(current_row, 0).text()
        return None
