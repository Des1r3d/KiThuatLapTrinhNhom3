"""
Shelf View — PHARMA.SYS Shelf Management Table.

Uses Qt Designer-generated UI from shelf_view_ui.py for layout.
Features:
- Table displaying all shelves with columns:
  ID, Dãy, Cột, Sức chứa, Đã dùng, Còn lại
- Add / Edit / Delete shelf operations
- Context menu (right-click) for edit/delete
- Double-click to edit
- Capacity usage visualization
"""
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QMenu, QHeaderView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QAction

from src.models import Shelf
from src.ui.theme import Theme
from src.ui.generated.shelf_view_ui import Ui_ShelfView


class ShelfView(QWidget):
    """
    Widget for displaying and managing shelves in a table.

    Uses Ui_ShelfView from shelf_view_ui.py for layout.

    Features:
    - Table with shelf info and capacity usage
    - Add/Edit/Delete actions
    - Context menu for quick actions
    - Double-click to edit

    Signals:
        add_requested: Emitted when Add button is clicked
        edit_requested: Emitted with shelf_id when edit is requested
        delete_requested: Emitted with shelf_id when delete is requested
    """

    add_requested = pyqtSignal()
    edit_requested = pyqtSignal(str)     # shelf_id
    delete_requested = pyqtSignal(str)   # shelf_id

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
        self._medicines_per_shelf: dict = {}  # shelf_id -> used quantity

        self.setup_ui()

    def setup_ui(self):
        """Setup shelf table UI using Qt Designer generated class."""
        self.ui = Ui_ShelfView()
        self.ui.setupUi(self)

        # Configure column widths (not in .ui)
        header = self.ui.tbl_shelves.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        # Row height
        self.ui.tbl_shelves.verticalHeader().setDefaultSectionSize(42)

        # Connect signals
        self.ui.btn_add.clicked.connect(lambda: self.add_requested.emit())
        self.ui.tbl_shelves.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.ui.tbl_shelves.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.tbl_shelves.customContextMenuRequested.connect(
            self.show_context_menu
        )

    def load_shelves(
        self,
        shelves: List[Shelf],
        medicines_per_shelf: Optional[dict] = None
    ):
        """
        Load shelves into table.

        Args:
            shelves: List of Shelf objects to display
            medicines_per_shelf: Dict mapping shelf_id -> used quantity
        """
        self.shelves = shelves
        self._medicines_per_shelf = medicines_per_shelf or {}

        self.ui.tbl_shelves.setSortingEnabled(False)
        self.ui.tbl_shelves.setRowCount(0)

        for shelf in self.shelves:
            self.add_shelf_row(shelf)

        self.ui.tbl_shelves.setSortingEnabled(True)
        self.ui.lbl_count.setText(f"{len(shelves)} kệ")

    def add_shelf_row(self, shelf: Shelf):
        """
        Add a single shelf row to table.

        Args:
            shelf: Shelf object to add
        """
        row = self.ui.tbl_shelves.rowCount()
        self.ui.tbl_shelves.insertRow(row)

        # ID
        id_item = QTableWidgetItem(shelf.id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tbl_shelves.setItem(row, 0, id_item)

        # Column (Dãy - letter)
        col_item = QTableWidgetItem(shelf.column)
        col_item.setFlags(col_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        col_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_shelves.setItem(row, 1, col_item)

        # Row (Cột - number)
        row_item = QTableWidgetItem(shelf.row)
        row_item.setFlags(row_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        row_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_shelves.setItem(row, 2, row_item)

        # Capacity
        try:
            cap = int(shelf.capacity)
        except (ValueError, TypeError):
            cap = 0
        cap_item = QTableWidgetItem(str(cap))
        cap_item.setData(Qt.ItemDataRole.UserRole, cap)
        cap_item.setFlags(cap_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        cap_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_shelves.setItem(row, 3, cap_item)

        # Used
        used = self._medicines_per_shelf.get(shelf.id, 0)
        used_item = QTableWidgetItem(str(used))
        used_item.setData(Qt.ItemDataRole.UserRole, used)
        used_item.setFlags(used_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        used_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tbl_shelves.setItem(row, 4, used_item)

        # Remaining
        remaining = cap - used
        rem_item = QTableWidgetItem(str(remaining))
        rem_item.setData(Qt.ItemDataRole.UserRole, remaining)
        rem_item.setFlags(rem_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        rem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Color code remaining capacity
        if remaining <= 0:
            rem_item.setForeground(QColor(Theme.CHART_RED))
            rem_font = rem_item.font()
            rem_font.setBold(True)
            rem_item.setFont(rem_font)
        elif remaining <= cap * 0.2:
            rem_item.setForeground(QColor(Theme.CHART_ORANGE))
            rem_font = rem_item.font()
            rem_font.setBold(True)
            rem_item.setFont(rem_font)

        self.ui.tbl_shelves.setItem(row, 5, rem_item)

    def on_item_double_clicked(self, item: QTableWidgetItem):
        """Handle double-click on table item."""
        row = item.row()
        shelf_id = self.ui.tbl_shelves.item(row, 0).text()
        self.edit_requested.emit(shelf_id)

    def show_context_menu(self, position):
        """
        Show context menu for table row.

        Args:
            position: Position where menu was requested
        """
        item = self.ui.tbl_shelves.itemAt(position)
        if not item:
            return

        row = item.row()
        shelf_id = self.ui.tbl_shelves.item(row, 0).text()

        menu = QMenu(self)

        # Edit action
        edit_action = QAction("Chỉnh sửa kệ", self)
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(shelf_id)
        )
        menu.addAction(edit_action)

        # Delete action
        delete_action = QAction("Xóa kệ", self)
        delete_action.triggered.connect(
            lambda: self.delete_requested.emit(shelf_id)
        )
        menu.addAction(delete_action)

        menu.exec(self.ui.tbl_shelves.viewport().mapToGlobal(position))

    def get_selected_shelf_id(self) -> Optional[str]:
        """
        Get ID of currently selected shelf.

        Returns:
            Shelf ID if a row is selected, None otherwise
        """
        current_row = self.ui.tbl_shelves.currentRow()
        if current_row >= 0:
            return self.ui.tbl_shelves.item(current_row, 0).text()
        return None
