"""
Main Window for Pharmacy Management System — PHARMA.SYS.

Features:
- Dark sidebar navigation (fixed #0D1F3C)
- Top bar with page title, search hint, theme toggle
- Stacked widget for different views
- Keyboard shortcuts (Ctrl+K, Ctrl+N, Ctrl+D)
- Global search modal
"""
from typing import Optional, List

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QListWidgetItem,
    QPushButton, QStatusBar, QMessageBox, QDialog,
    QLineEdit, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut, QFont, QAction

from src.inventory_manager import InventoryManager
from src.search_engine import SearchEngine
from src.image_manager import ImageManager
from src.models import Medicine
from src.ui.theme import Theme, ThemeMode
from src.ui.dashboard import Dashboard
from src.ui.inventory_view import InventoryView
from src.ui.medicine_dialog import MedicineDialog
from src.ui.shelf_dialog import ShelfDialog
from src.ui.shelf_view import ShelfView
from src.ui.generated.search import Ui_dlg_search
from src.ui.notification_dialogs import (
    AddSuccessDialog, EditSuccessDialog, DeleteSuccessDialog,
    ConfirmDeleteDialog, ShelfFullErrorDialog
)
from src.ui.medicine_detail_view import MedicineDetailView
from src.ui.filter_dialog import FilterMedicineDialog


class SearchModal(QDialog):
    """
    Global search modal accessible via Ctrl+K.

    Uses Ui_dlg_search from Qt Designer for layout.

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

    def setup_ui(self):
        """Setup search modal UI using Qt Designer generated class."""
        self.ui = Ui_dlg_search()
        self.ui.setupUi(self)

        self.setWindowTitle("Tìm kiếm nhanh")
        self.setModal(True)

        # Connect signals
        self.ui.txt_search.textChanged.connect(self.on_search)
        self.ui.list_results.itemDoubleClicked.connect(self.on_result_selected)
        self.ui.txt_search.returnPressed.connect(self.select_first_result)

    def showEvent(self, event):
        """Focus search input when modal is shown."""
        super().showEvent(event)
        self.ui.txt_search.setFocus()
        self.ui.txt_search.clear()
        self.ui.list_results.clear()

    def on_search(self, query: str):
        """
        Perform search when query changes.

        Args:
            query: Search query string
        """
        self.ui.list_results.clear()

        if not query or len(query) < 2:
            return

        # Search medicines
        results = self.search_engine.search(query, limit=10)

        if not results:
            item = QListWidgetItem("Không tìm thấy kết quả")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.ui.list_results.addItem(item)
            return

        # Display results
        for medicine, score in results:
            display_text = f"{medicine.name} - {medicine.shelf_id} ({score}%)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, medicine.id)
            self.ui.list_results.addItem(item)

    def on_result_selected(self, item: QListWidgetItem):
        """Handle result selection."""
        medicine_id = item.data(Qt.ItemDataRole.UserRole)
        if medicine_id:
            self.medicine_selected.emit(medicine_id)
            self.accept()

    def select_first_result(self):
        """Select first result in list."""
        if self.ui.list_results.count() > 0:
            first_item = self.ui.list_results.item(0)
            if first_item.flags() & Qt.ItemFlag.ItemIsEnabled:
                self.on_result_selected(first_item)

    def apply_theme(self):
        """Apply theme stylesheet."""
        pass  # Uses Qt Designer inline styles


class MainWindow(QMainWindow):
    """
    Main application window — PHARMA.SYS.

    Features:
    - Dark sidebar navigation (Dashboard, Inventory, Shelf Mgmt)
    - Top bar with search hint, theme toggle, add button
    - Keyboard shortcuts
    - Theme toggle (Light/Dark)
    - Global search (Ctrl+K)
    - Status bar
    """

    # Page title mapping
    PAGE_TITLES = [
        "Dashboard Overview",
        "Inventory Management",
        "Shelf Management"
    ]

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        # Initialize managers
        self.inventory_manager = InventoryManager()
        self.search_engine = SearchEngine()
        self.image_manager = ImageManager()
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
        self.setWindowTitle("PHARMA.SYS — Hệ Thống Quản Lý Kho Thuốc")
        self.setMinimumSize(1200, 800)

        # Central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # ── Right side (top bar + content) ──
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Top bar
        topbar = self.create_topbar()
        right_layout.addWidget(topbar)

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
            Theme.SPACING_BASE * 2,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3
        )

        # Inventory view
        self.inventory_view = InventoryView(theme=self.theme)
        self.inventory_view.edit_requested.connect(self.show_edit_medicine_dialog)
        self.inventory_view.delete_requested.connect(self.delete_medicine)
        inventory_layout.addWidget(self.inventory_view)

        self.content_stack.addWidget(inventory_container)

        # Shelf management page
        shelf_container = QWidget()
        shelf_layout = QVBoxLayout(shelf_container)
        shelf_layout.setContentsMargins(
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 2,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3
        )

        # Shelf toolbar
        shelf_toolbar = QHBoxLayout()

        self.add_shelf_button = QPushButton("➕ Thêm kệ mới")
        self.add_shelf_button.clicked.connect(self.show_add_shelf_dialog)
        shelf_toolbar.addWidget(self.add_shelf_button)

        shelf_toolbar.addStretch()
        shelf_layout.addLayout(shelf_toolbar)

        # Shelf view
        self.shelf_view = ShelfView(theme=self.theme)
        self.shelf_view.edit_requested.connect(self.show_edit_shelf_dialog)
        self.shelf_view.delete_requested.connect(self.delete_shelf)
        shelf_layout.addWidget(self.shelf_view)

        self.content_stack.addWidget(shelf_container)

        right_layout.addWidget(self.content_stack, 1)
        main_layout.addWidget(right_container, 1)

        self.setCentralWidget(central_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("● System Ready")

    def create_sidebar(self) -> QWidget:
        """
        Create dark sidebar navigation.

        Returns:
            Sidebar QFrame widget
        """
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFrameShape(QFrame.Shape.NoFrame)
        sidebar.setMinimumWidth(220)
        sidebar.setMaximumWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Logo section ──
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 24, 20, 24)

        logo_icon = QLabel("💊")
        logo_font = QFont()
        logo_font.setPointSize(20)
        logo_icon.setFont(logo_font)
        logo_layout.addWidget(logo_icon)

        logo_text = QLabel("PHARMA.SYS")
        logo_text.setObjectName("logo_label")
        logo_font_text = QFont()
        logo_font_text.setPointSize(16)
        logo_font_text.setBold(True)
        logo_text.setFont(logo_font_text)
        logo_layout.addWidget(logo_text)

        logo_layout.addStretch()
        layout.addWidget(logo_container)

        # ── Navigation list ──
        self.nav_list = QListWidget()
        self.nav_list.addItem("📊  Dashboard")
        self.nav_list.addItem("📦  Inventory")
        self.nav_list.addItem("🗄️  Shelves")

        # Disabled items
        reports_item = QListWidgetItem("📋  Reports")
        reports_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.nav_list.addItem(reports_item)

        settings_item = QListWidgetItem("⚙️  Settings")
        settings_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.nav_list.addItem(settings_item)

        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.on_nav_changed)
        layout.addWidget(self.nav_list)

        layout.addStretch()

        # ── Theme toggle ──
        self.theme_button = QPushButton("🌙 Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setContentsMargins(16, 8, 16, 8)

        theme_container = QWidget()
        theme_layout = QVBoxLayout(theme_container)
        theme_layout.setContentsMargins(12, 8, 12, 16)
        theme_layout.addWidget(self.theme_button)
        layout.addWidget(theme_container)

        return sidebar

    def create_topbar(self) -> QWidget:
        """
        Create top bar with page title, search, and actions.

        Returns:
            Top bar QFrame widget
        """
        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setFrameShape(QFrame.Shape.NoFrame)
        topbar.setFixedHeight(60)

        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)

        # Page title (dynamic)
        self.page_title_label = QLabel("Dashboard Overview")
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H1)
        title_font.setBold(True)
        self.page_title_label.setFont(title_font)
        layout.addWidget(self.page_title_label)

        layout.addStretch()

        # Search hint
        search_hint = QPushButton("🔍  Ctrl+K to Search")
        search_hint.setProperty("secondary", True)
        search_hint.setFixedWidth(180)
        search_hint.clicked.connect(self.show_search_modal)
        layout.addWidget(search_hint)

        # Theme toggle (icon only)
        self.topbar_theme_btn = QPushButton("🌙")
        self.topbar_theme_btn.setProperty("secondary", True)
        self.topbar_theme_btn.setFixedWidth(36)
        self.topbar_theme_btn.setToolTip("Toggle Theme (Ctrl+D)")
        self.topbar_theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.topbar_theme_btn)

        # Add medicine button
        self.add_button = QPushButton("➕ Add Medicine")
        self.add_button.clicked.connect(self.show_add_medicine_dialog)
        self.add_button.setFixedWidth(160)
        layout.addWidget(self.add_button)

        return topbar

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
        # Only handle valid page indices (0-2)
        if index < 0 or index > 2:
            return

        self.content_stack.setCurrentIndex(index)

        # Update page title
        self.page_title_label.setText(self.PAGE_TITLES[index])

        # Refresh data when switching views
        if index == 0:  # Dashboard
            self.refresh_dashboard()
        elif index == 1:  # Inventory
            self.refresh_inventory()
        elif index == 2:  # Shelf Management
            self.refresh_shelf_view()

    def show_add_medicine_dialog(self):
        """Show dialog to add new medicine."""
        dialog = MedicineDialog(
            parent=self,
            medicine=None,
            shelves=self.inventory_manager.get_all_shelves(),
            theme=self.theme,
            image_manager=self.image_manager
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            medicine = dialog.get_medicine()
            if medicine:
                try:
                    added = self.inventory_manager.add_medicine(medicine)

                    # Handle image upload
                    image_source = dialog.get_selected_image_path()
                    if image_source and added.id:
                        try:
                            rel_path = self.image_manager.save_image(
                                image_source, added.id
                            )
                            self.inventory_manager.update_medicine(
                                added.id, {"image_path": rel_path}
                            )
                        except (IOError, ValueError) as img_err:
                            QMessageBox.warning(
                                self, "Cảnh báo",
                                f"Thuốc đã thêm nhưng không lưu được ảnh: {str(img_err)}"
                            )

                    self.refresh_all_views()
                    self.search_engine.update_index(
                        self.inventory_manager.get_all_medicines()
                    )
                    self.status_bar.showMessage(
                        f"✅ Đã thêm thuốc: {medicine.name}", 3000
                    )

                    # Show success notification
                    success_dlg = AddSuccessDialog(
                        self, medicine.name, added.id
                    )
                    success_dlg.exec()

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
            theme=self.theme,
            image_manager=self.image_manager
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_medicine = dialog.get_medicine()
            if updated_medicine:
                try:
                    # Handle image changes
                    image_path = medicine.image_path  # Keep existing by default
                    image_source = dialog.get_selected_image_path()

                    if image_source:
                        # New image uploaded
                        try:
                            image_path = self.image_manager.save_image(
                                image_source, medicine_id
                            )
                        except (IOError, ValueError) as img_err:
                            QMessageBox.warning(
                                self, "Cảnh báo",
                                f"Không lưu được ảnh: {str(img_err)}"
                            )
                            image_path = medicine.image_path
                    elif dialog.is_image_removed():
                        # Image explicitly removed
                        self.image_manager.delete_image(medicine_id)
                        image_path = ""

                    # Create changes dict
                    changes = {
                        'name': updated_medicine.name,
                        'quantity': updated_medicine.quantity,
                        'expiry_date': updated_medicine.expiry_date,
                        'shelf_id': updated_medicine.shelf_id,
                        'price': updated_medicine.price,
                        'image_path': image_path
                    }
                    self.inventory_manager.update_medicine(
                        medicine_id, changes
                    )
                    self.refresh_all_views()
                    self.search_engine.update_index(
                        self.inventory_manager.get_all_medicines()
                    )
                    self.status_bar.showMessage(
                        f"✅ Đã cập nhật thuốc: {updated_medicine.name}", 3000
                    )

                    # Show success notification
                    success_dlg = EditSuccessDialog(
                        self, updated_medicine.name, medicine_id
                    )
                    success_dlg.exec()

                except ValueError as e:
                    QMessageBox.warning(
                        self, "Lỗi", f"Không thể cập nhật: {str(e)}"
                    )

    def delete_medicine(self, medicine_id: str):
        """
        Delete a medicine and its associated image.

        Args:
            medicine_id: ID of medicine to delete
        """
        try:
            medicine = self.inventory_manager.get_medicine(medicine_id)

            # Delete associated image
            self.image_manager.delete_image(medicine_id)

            self.inventory_manager.remove_medicine(medicine_id)
            self.refresh_all_views()
            self.search_engine.update_index(
                self.inventory_manager.get_all_medicines()
            )
            if medicine:
                self.status_bar.showMessage(
                    f"🗑️ Đã xóa thuốc: {medicine.name}", 3000
                )

                # Show success notification
                success_dlg = DeleteSuccessDialog(
                    self, medicine.name, medicine_id
                )
                success_dlg.exec()

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

        self.status_bar.showMessage(
            f"🔍 Đã chọn thuốc ID: {medicine_id}", 3000
        )

    def toggle_theme(self):
        """Toggle between Light and Dark themes."""
        new_mode = self.theme.toggle_mode()

        if new_mode == ThemeMode.DARK:
            self.theme_button.setText("☀️ Light Mode")
            self.topbar_theme_btn.setText("☀️")
        else:
            self.theme_button.setText("🌙 Dark Mode")
            self.topbar_theme_btn.setText("🌙")

        self.apply_theme()
        self.status_bar.showMessage(
            f"🎨 Switched to {new_mode.value} mode", 2000
        )

    def refresh_all_views(self):
        """Refresh all data views."""
        self.refresh_dashboard()
        self.refresh_inventory()
        self.refresh_shelf_view()

    def refresh_dashboard(self):
        """Refresh dashboard data."""
        medicines = self.inventory_manager.get_all_medicines()
        self.dashboard.load_data(medicines)

    def refresh_inventory(self):
        """Refresh inventory table."""
        medicines = self.inventory_manager.get_all_medicines()
        self.inventory_view.load_medicines(medicines)

    def refresh_shelf_view(self):
        """Refresh shelf view with current data."""
        shelves = self.inventory_manager.get_all_shelves()
        medicines = self.inventory_manager.get_all_medicines()
        self.shelf_view.load_shelves(shelves, medicines)

    def show_add_shelf_dialog(self):
        """Show dialog to add new shelf."""
        dialog = ShelfDialog(
            parent=self,
            shelf=None,
            theme=self.theme
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            shelf = dialog.get_shelf()
            if shelf:
                try:
                    self.inventory_manager.add_shelf(shelf)
                    self.refresh_shelf_view()
                    self.status_bar.showMessage(
                        f"✅ Đã thêm kệ: {shelf.id}", 3000
                    )
                except ValueError as e:
                    QMessageBox.warning(
                        self, "Lỗi", f"Không thể thêm kệ: {str(e)}"
                    )

    def show_edit_shelf_dialog(self, shelf_id: str):
        """Show dialog to edit existing shelf."""
        shelf = self.inventory_manager.get_shelf(shelf_id)
        if not shelf:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy kệ")
            return

        dialog = ShelfDialog(
            parent=self,
            shelf=shelf,
            theme=self.theme
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_shelf = dialog.get_shelf()
            if updated_shelf:
                try:
                    changes = {
                        'row': updated_shelf.row,
                        'column': updated_shelf.column,
                        'capacity': updated_shelf.capacity
                    }
                    self.inventory_manager.update_shelf(shelf_id, changes)
                    self.refresh_shelf_view()
                    self.status_bar.showMessage(
                        f"✅ Đã cập nhật kệ: {shelf_id}", 3000
                    )
                except ValueError as e:
                    QMessageBox.warning(
                        self, "Lỗi", f"Không thể cập nhật: {str(e)}"
                    )

    def delete_shelf(self, shelf_id: str):
        """Delete a shelf."""
        try:
            self.inventory_manager.remove_shelf(shelf_id)
            self.refresh_shelf_view()
            self.status_bar.showMessage(
                f"🗑️ Đã xóa kệ: {shelf_id}", 3000
            )
        except ValueError as e:
            QMessageBox.warning(
                self, "Lỗi", f"Không thể xóa kệ: {str(e)}"
            )

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

        self.shelf_view.theme = self.theme
        self.shelf_view.apply_theme()
        self.shelf_view.refresh()
