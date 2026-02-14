"""
Main Window for Pharmacy Management System.

Features:
- Sidebar navigation
- Stacked widget for different views
- Keyboard shortcuts (Ctrl+K, Ctrl+N, Ctrl+D)
- Theme toggle
- Global search modal
"""
from typing import Optional, List

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QListWidgetItem,
    QPushButton, QStatusBar, QMessageBox, QDialog,
    QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut, QFont, QAction

from src.inventory_manager import InventoryManager
from src.search_engine import SearchEngine
from src.models import Medicine
from src.ui.theme import Theme, ThemeMode
from src.ui.dashboard import Dashboard
from src.ui.inventory_view import InventoryView
from src.ui.medicine_dialog import MedicineDialog


class SearchModal(QDialog):
    """
    Global search modal accessible via Ctrl+K.
    
    Features:
    - Fuzzy search
    - Real-time results
    - Keyboard navigation
    """
    
    medicine_selected = pyqtSignal(str)  # medicine_id
    
    def __init__(
        self, 
        parent=None, 
        search_engine: Optional[SearchEngine] = None,
        theme: Optional[Theme] = None
    ):
        """
        Initialize search modal.
        
        Args:
            parent: Parent widget
            search_engine: SearchEngine instance
            theme: Theme instance
        """
        super().__init__(parent)
        
        self.search_engine = search_engine or SearchEngine()
        self.theme = theme or Theme()
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup search modal UI."""
        self.setWindowTitle("Tìm kiếm nhanh")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_BASE * 2)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên thuốc để tìm kiếm...")
        search_font = QFont()
        search_font.setPointSize(Theme.FONT_SIZE_H2)
        self.search_input.setFont(search_font)
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.on_result_selected)
        layout.addWidget(self.results_list)
        
        # Hint label
        hint_label = QLabel("💡 Gợi ý: Nhấn Enter để chọn kết quả đầu tiên")
        hint_label.setProperty("secondary", True)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_label)
        
        self.setLayout(layout)
        
        # Enter key to select first result
        self.search_input.returnPressed.connect(self.select_first_result)
    
    def showEvent(self, event):
        """Focus search input when modal is shown."""
        super().showEvent(event)
        self.search_input.setFocus()
        self.search_input.clear()
        self.results_list.clear()
    
    def on_search(self, query: str):
        """
        Perform search when query changes.
        
        Args:
            query: Search query string
        """
        self.results_list.clear()
        
        if not query or len(query) < 2:
            return
        
        # Search medicines
        results = self.search_engine.search(query, limit=10)
        
        if not results:
            item = QListWidgetItem("Không tìm thấy kết quả")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.results_list.addItem(item)
            return
        
        # Display results
        for medicine, score in results:
            display_text = f"{medicine.name} - {medicine.shelf_id} ({score}%)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, medicine.id)
            self.results_list.addItem(item)
    
    def on_result_selected(self, item: QListWidgetItem):
        """Handle result selection."""
        medicine_id = item.data(Qt.ItemDataRole.UserRole)
        if medicine_id:
            self.medicine_selected.emit(medicine_id)
            self.accept()
    
    def select_first_result(self):
        """Select first result in list."""
        if self.results_list.count() > 0:
            first_item = self.results_list.item(0)
            if first_item.flags() & Qt.ItemFlag.ItemIsEnabled:
                self.on_result_selected(first_item)
    
    def apply_theme(self):
        """Apply theme stylesheet."""
        self.setStyleSheet(self.theme.get_stylesheet())


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Features:
    - Sidebar navigation (Dashboard, Inventory)
    - Keyboard shortcuts
    - Theme toggle (Light/Dark)
    - Global search (Ctrl+K)
    - Status bar
    """
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize managers
        self.inventory_manager = InventoryManager()
        self.search_engine = SearchEngine()
        self.theme = Theme(ThemeMode.LIGHT)
        
        # Load data
        try:
            self.inventory_manager.load_data()
            self.search_engine.index_data(
                self.inventory_manager.get_all_medicines()
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Lỗi tải dữ liệu",
                f"Không thể tải dữ liệu: {str(e)}"
            )
        
        self.setup_ui()
        self.setup_shortcuts()
        self.apply_theme()
        
        # Initial data load
        self.refresh_all_views()
    
    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle("Hệ Thống Quản Lý Kho Thuốc")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Main content area
        self.content_stack = QStackedWidget()
        
        # Dashboard page
        self.dashboard = Dashboard(theme=self.theme)
        self.content_stack.addWidget(self.dashboard)
        
        # Inventory page
        inventory_container = QWidget()
        inventory_layout = QVBoxLayout(inventory_container)
        inventory_layout.setContentsMargins(
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3
        )
        
        # Inventory toolbar
        toolbar_layout = QHBoxLayout()
        
        self.add_button = QPushButton("➕ Thêm thuốc mới (Ctrl+N)")
        self.add_button.clicked.connect(self.show_add_medicine_dialog)
        toolbar_layout.addWidget(self.add_button)
        
        toolbar_layout.addStretch()
        
        self.search_button = QPushButton("🔍 Tìm kiếm (Ctrl+K)")
        self.search_button.clicked.connect(self.show_search_modal)
        toolbar_layout.addWidget(self.search_button)
        
        inventory_layout.addLayout(toolbar_layout)
        
        # Inventory view
        self.inventory_view = InventoryView(theme=self.theme)
        self.inventory_view.edit_requested.connect(self.show_edit_medicine_dialog)
        self.inventory_view.delete_requested.connect(self.delete_medicine)
        inventory_layout.addWidget(self.inventory_view)
        
        self.content_stack.addWidget(inventory_container)
        
        main_layout.addWidget(self.content_stack, 1)
        
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng")
    
    def create_sidebar(self) -> QWidget:
        """
        Create sidebar navigation.
        
        Returns:
            Sidebar widget
        """
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setMinimumWidth(220)
        sidebar.setMaximumWidth(220)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(
            Theme.SPACING_BASE,
            Theme.SPACING_BASE * 2,
            Theme.SPACING_BASE,
            Theme.SPACING_BASE * 2
        )
        
        # App title
        title_label = QLabel("💊 Kho Thuốc")
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H1)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(Theme.SPACING_BASE * 3)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.addItem("📊 Bảng điều khiển")
        self.nav_list.addItem("📦 Danh sách thuốc")
        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.on_nav_changed)
        layout.addWidget(self.nav_list)
        
        layout.addStretch()
        
        # Theme toggle button
        self.theme_button = QPushButton("🌙 Chế độ tối (Ctrl+D)")
        self.theme_button.setProperty("secondary", True)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)
        
        return sidebar
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Ctrl+K - Search
        search_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        search_shortcut.activated.connect(self.show_search_modal)
        
        # Ctrl+N - Add medicine
        add_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        add_shortcut.activated.connect(self.show_add_medicine_dialog)
        
        # Ctrl+D - Toggle theme
        theme_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        theme_shortcut.activated.connect(self.toggle_theme)
    
    def on_nav_changed(self, index: int):
        """
        Handle navigation change.
        
        Args:
            index: Selected navigation index
        """
        self.content_stack.setCurrentIndex(index)
        
        # Refresh data when switching views
        if index == 0:  # Dashboard
            self.refresh_dashboard()
        elif index == 1:  # Inventory
            self.refresh_inventory()
    
    def show_add_medicine_dialog(self):
        """Show dialog to add new medicine."""
        dialog = MedicineDialog(
            parent=self,
            medicine=None,
            shelves=self.inventory_manager.get_all_shelves(),
            theme=self.theme
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            medicine = dialog.get_medicine()
            if medicine:
                try:
                    self.inventory_manager.add_medicine(medicine)
                    self.refresh_all_views()
                    self.search_engine.update_index(
                        self.inventory_manager.get_all_medicines()
                    )
                    self.status_bar.showMessage(
                        f"Đã thêm thuốc: {medicine.name}", 3000
                    )
                except ValueError as e:
                    QMessageBox.warning(
                        self, "Lỗi", f"Không thể thêm thuốc: {str(e)}"
                    )
    
    def show_edit_medicine_dialog(self, medicine_id: str):
        """
        Show dialog to edit medicine.
        
        Args:
            medicine_id: ID of medicine to edit
        """
        medicine = self.inventory_manager.get_medicine(medicine_id)
        if not medicine:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy thuốc")
            return
        
        dialog = MedicineDialog(
            parent=self,
            medicine=medicine,
            shelves=self.inventory_manager.get_all_shelves(),
            theme=self.theme
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_medicine = dialog.get_medicine()
            if updated_medicine:
                try:
                    # Create changes dict
                    changes = {
                        'name': updated_medicine.name,
                        'quantity': updated_medicine.quantity,
                        'expiry_date': updated_medicine.expiry_date,
                        'shelf_id': updated_medicine.shelf_id,
                        'price': updated_medicine.price
                    }
                    self.inventory_manager.update_medicine(
                        medicine_id, changes
                    )
                    self.refresh_all_views()
                    self.search_engine.update_index(
                        self.inventory_manager.get_all_medicines()
                    )
                    self.status_bar.showMessage(
                        f"Đã cập nhật thuốc: {updated_medicine.name}", 3000
                    )
                except ValueError as e:
                    QMessageBox.warning(
                        self, "Lỗi", f"Không thể cập nhật: {str(e)}"
                    )
    
    def delete_medicine(self, medicine_id: str):
        """
        Delete a medicine.
        
        Args:
            medicine_id: ID of medicine to delete
        """
        try:
            medicine = self.inventory_manager.get_medicine(medicine_id)
            self.inventory_manager.remove_medicine(medicine_id)
            self.refresh_all_views()
            self.search_engine.update_index(
                self.inventory_manager.get_all_medicines()
            )
            if medicine:
                self.status_bar.showMessage(
                    f"Đã xóa thuốc: {medicine.name}", 3000
                )
        except ValueError as e:
            QMessageBox.warning(
                self, "Lỗi", f"Không thể xóa thuốc: {str(e)}"
            )
    
    def show_search_modal(self):
        """Show global search modal."""
        modal = SearchModal(
            parent=self,
            search_engine=self.search_engine,
            theme=self.theme
        )
        modal.medicine_selected.connect(self.on_search_result_selected)
        modal.exec()
    
    def on_search_result_selected(self, medicine_id: str):
        """
        Handle search result selection.
        
        Args:
            medicine_id: Selected medicine ID
        """
        # Switch to inventory view
        self.nav_list.setCurrentRow(1)
        self.content_stack.setCurrentIndex(1)
        
        # TODO: Highlight selected medicine in table
        self.status_bar.showMessage(
            f"Đã chọn thuốc ID: {medicine_id}", 3000
        )
    
    def toggle_theme(self):
        """Toggle between Light and Dark themes."""
        new_mode = self.theme.toggle_mode()
        
        if new_mode == ThemeMode.DARK:
            self.theme_button.setText("☀️ Chế độ sáng (Ctrl+D)")
        else:
            self.theme_button.setText("🌙 Chế độ tối (Ctrl+D)")
        
        self.apply_theme()
        self.status_bar.showMessage(
            f"Đã chuyển sang chế độ {new_mode.value}", 2000
        )
    
    def refresh_all_views(self):
        """Refresh all data views."""
        self.refresh_dashboard()
        self.refresh_inventory()
    
    def refresh_dashboard(self):
        """Refresh dashboard data."""
        medicines = self.inventory_manager.get_all_medicines()
        self.dashboard.load_data(medicines)
    
    def refresh_inventory(self):
        """Refresh inventory table."""
        medicines = self.inventory_manager.get_all_medicines()
        self.inventory_view.load_medicines(medicines)
    
    def apply_theme(self):
        """Apply current theme to all components."""
        stylesheet = self.theme.get_stylesheet()
        self.setStyleSheet(stylesheet)
        
        # Apply to child widgets
        self.dashboard.theme = self.theme
        self.dashboard.apply_theme()
        self.dashboard.update_charts()  # Redraw charts with new theme
        
        self.inventory_view.theme = self.theme
        self.inventory_view.apply_theme()
        self.inventory_view.refresh()  # Reapply row colors
