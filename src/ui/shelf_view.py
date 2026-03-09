"""
Shelf View - Table display for shelf management.

Features:
- Table view with shelf information
- Context menu (Edit, Delete)
- Double-click to edit
- Medicine count per shelf
"""
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMenu,
    QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction

from src.models import Shelf, Medicine
from src.ui.theme import Theme


class ShelfView(QWidget):
    """
    Widget for displaying shelves in a table.
    
    Features:
    - Shows shelf ID, row, column, capacity
    - Shows count of medicines on each shelf
    - Context menu for Edit/Delete
    - Double-click to edit
    
    Signals:
        edit_requested: Emitted when edit is requested (shelf_id)
        delete_requested: Emitted when delete is requested (shelf_id)
    """
    
    edit_requested = pyqtSignal(str)    # shelf_id
    delete_requested = pyqtSignal(str)  # shelf_id
    
    def __init__(self, parent=None, theme: Optional[Theme] = None):
        """
        Initialize Shelf View.
        
        Args:
            parent: Parent widget
            theme: Theme instance for styling
        """
        super().__init__(parent)
        
        self.theme = theme or Theme()
        self.shelves: List[Shelf] = []
        self.medicines: List[Medicine] = []
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup table UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Danh Sách Kệ Thuốc")
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H2)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.count_label = QLabel("0 kệ")
        self.count_label.setProperty("secondary", True)
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Mã Kệ", "Khu", "Cột", "Dãy", "Sức Chứa", "Số Thuốc"
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
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # Context menu
        self.table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table.customContextMenuRequested.connect(
            self.show_context_menu
        )
        
        # Double-click to edit
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_shelves(self, shelves: List[Shelf], medicines: List[Medicine]):
        """
        Load shelves into table.
        
        Args:
            shelves: List of Shelf objects to display
            medicines: List of Medicine objects (to count per shelf)
        """
        self.shelves = shelves
        self.medicines = medicines
        self.refresh_table()
    
    def refresh_table(self):
        """Refresh table with current shelf data."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for shelf in self.shelves:
            self.add_shelf_row(shelf)
        
        self.table.setSortingEnabled(True)
        self.count_label.setText(f"{len(self.shelves)} kệ")
    
    def add_shelf_row(self, shelf: Shelf):
        """
        Add a single shelf row to table.
        
        Args:
            shelf: Shelf object to add
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # ID
        id_item = QTableWidgetItem(shelf.id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 0, id_item)
        
        # Zone (Khu)
        zone_item = QTableWidgetItem(shelf.zone)
        zone_item.setFlags(zone_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 1, zone_item)
        
        # Column (Cột)
        col_item = QTableWidgetItem(shelf.column)
        col_item.setFlags(col_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 2, col_item)
        
        # Row (Dãy)
        row_item = QTableWidgetItem(shelf.row)
        row_item.setFlags(row_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 3, row_item)
        
        # Capacity
        capacity_item = QTableWidgetItem(f"{shelf.capacity}")
        capacity_item.setData(Qt.ItemDataRole.UserRole, int(shelf.capacity))
        capacity_item.setFlags(capacity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 4, capacity_item)
        
        # Medicine count on this shelf
        med_count = sum(
            1 for m in self.medicines if m.shelf_id == shelf.id
        )
        count_item = QTableWidgetItem(str(med_count))
        count_item.setData(Qt.ItemDataRole.UserRole, med_count)
        count_item.setFlags(count_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 5, count_item)
    
    def on_item_double_clicked(self, item: QTableWidgetItem):
        """Handle double-click on table item."""
        row = item.row()
        shelf_id = self.table.item(row, 0).text()
        self.edit_requested.emit(shelf_id)
    
    def show_context_menu(self, position):
        """Show context menu for shelf row."""
        item = self.table.itemAt(position)
        if not item:
            return
        
        row = item.row()
        shelf_id = self.table.item(row, 0).text()
        
        menu = QMenu(self)
        
        edit_action = QAction("✏️ Sửa kệ", self)
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(shelf_id)
        )
        menu.addAction(edit_action)
        
        delete_action = QAction("🗑️ Xóa kệ", self)
        delete_action.triggered.connect(
            lambda: self.confirm_delete(shelf_id)
        )
        menu.addAction(delete_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def confirm_delete(self, shelf_id: str):
        """
        Show confirmation dialog before deleting.
        
        Args:
            shelf_id: ID of shelf to delete
        """
        med_count = sum(
            1 for m in self.medicines if m.shelf_id == shelf_id
        )
        
        if med_count > 0:
            QMessageBox.warning(
                self,
                "Không thể xóa",
                f"Kệ '{shelf_id}' vẫn còn {med_count} thuốc.\n"
                "Vui lòng chuyển thuốc sang kệ khác trước khi xóa."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa kệ '{shelf_id}'?\n\n"
            "Thao tác này không thể hoàn tác.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(shelf_id)
    
    def refresh(self):
        """Refresh the table display."""
        self.refresh_table()
    
    def apply_theme(self):
        """Apply theme stylesheet."""
        self.setStyleSheet(self.theme.get_stylesheet())
