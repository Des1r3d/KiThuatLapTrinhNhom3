"""
Main Window — PHARMA.SYS Application.

The central hub for the Pharmacy Management System.
Features:
- Dark sidebar with navigation (Dashboard, Inventory, Shelves)
- Theme toggle (Light/Dark mode)
- Search dialog (Ctrl+K)
- Full CRUD for medicines and shelves
- Custom notification dialogs

This file contains ONLY business logic.
UI layout is defined in src/ui/generated/main_window_ui.py (Ui_MainWindow).
"""
import os
from typing import Optional, List

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QPushButton, QFrame, QMessageBox,
    QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QPixmap, QCloseEvent

from src.models import Medicine, Shelf
from src.inventory_manager import InventoryManager
from src.image_manager import ImageManager
from src.search_engine import SearchEngine
from src.ui.theme import Theme, ThemeMode
from src.ui.dashboard import Dashboard
from src.ui.inventory_view import InventoryView
from src.ui.shelf_view import ShelfView
from src.ui.medicine_dialog import MedicineDialog
from src.ui.shelf_dialog import ShelfDialog
from src.ui.medicine_detail_view import MedicineDetailView
from src.ui.filter_dialog import FilterMedicineDialog
from src.ui.notification_dialogs import (
    AddSuccessDialog, EditSuccessDialog, DeleteSuccessDialog,
    ConfirmDeleteDialog, ShelfFullErrorDialog
)
from src.ui.generated.search import Ui_dlg_search
from src.ui.generated.main_window_ui import Ui_MainWindow


class SearchDialog(QFrame):
    """
    Search dialog using generated UI from search.py.

    Provides fuzzy search for medicines with real-time results.
    Has a close button & supports Escape key to close.
    """

    def __init__(
        self,
        parent=None,
        search_engine: Optional[SearchEngine] = None,
        theme: Optional[Theme] = None
    ):
        super().__init__(parent)
        from PyQt6.QtWidgets import QDialog

        self.dialog = QDialog(parent)
        self.search_engine = search_engine or SearchEngine()
        self.theme = theme or Theme()
        self.selected_medicine_id: Optional[str] = None

        self.ui = Ui_dlg_search()
        self.ui.setupUi(self.dialog)

        self.dialog.setWindowTitle("Tìm kiếm thuốc")
        self.dialog.setWindowFlags(
            self.dialog.windowFlags() | Qt.WindowType.FramelessWindowHint
        )

        # Apply dark theme support
        c = self.theme._current_colors
        self.dialog.setStyleSheet(f"""
            QDialog {{ background-color: {c['surface']}; border: 1px solid {c['border']}; border-radius: 12px; }}
            QLineEdit#txt_search {{
                border: none; padding-left: 10px; font-size: 16px;
                color: {c['input_text']}; background-color: transparent;
            }}
            QListWidget {{ border: none; background-color: {c['surface']}; outline: none; color: {c['text_primary']}; }}
            QListWidget::item {{ border-bottom: 1px solid {c['border']}; padding: 8px; }}
            QListWidget::item:hover {{ background-color: {c['search_highlight']}; }}
        """)
        self.ui.frame_search.setStyleSheet(
            f"border-bottom: 1px solid {c['border']}; background-color: {c['table_row_alt']};"
        )

        # Add close button to search bar
        self.btn_close = QPushButton("Đóng")
        self.btn_close.setFixedSize(60, 30)
        self.btn_close.setStyleSheet(f"""
            QPushButton {{ background-color: {c['cancel_btn_bg']}; color: {c['text_primary']};
                border: 1px solid {c['border']}; border-radius: 6px; font-size: 12px; }}
            QPushButton:hover {{ border-color: {c['primary']}; color: {c['primary']}; }}
        """)
        self.btn_close.clicked.connect(self._on_close)
        self.ui.layout_h_search.addWidget(self.btn_close)

        # Connect search
        self.ui.txt_search.textChanged.connect(self._on_search)
        self.ui.list_results.itemClicked.connect(self._on_select)

        # Allow Escape key to close
        close_shortcut = QShortcut(QKeySequence("Escape"), self.dialog)
        close_shortcut.activated.connect(self._on_close)

    def _on_close(self):
        """Close the search dialog."""
        self.dialog.reject()

    def _on_search(self, text: str):
        """Handle search text change."""
        self.ui.list_results.clear()

        if not text.strip():
            return

        results = self.search_engine.search(text, limit=10)

        for medicine, score in results:
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(
                f"{medicine.name}  (Mã: {medicine.id}, "
                f"Kệ: {medicine.shelf_id}, Độ khớp: {score}%)"
            )
            item.setData(Qt.ItemDataRole.UserRole, medicine.id)
            self.ui.list_results.addItem(item)

    def _on_select(self, item):
        """Handle result selection (single click)."""
        self.selected_medicine_id = item.data(Qt.ItemDataRole.UserRole)
        self.dialog.accept()

    def exec(self) -> int:
        """Show dialog and return result."""
        self.ui.txt_search.clear()
        self.ui.list_results.clear()
        self.selected_medicine_id = None
        return self.dialog.exec()


class MainWindow(QMainWindow):
    """
    Main application window with sidebar navigation.

    Uses Ui_MainWindow (generated) for layout.
    This class handles ONLY business logic:
    - CRUD operations for medicines and shelves
    - Navigation and page switching
    - Theme toggling
    - Search functionality
    - Signal/Slot connections
    """

    # Navigation page indices
    PAGE_DASHBOARD = 0
    PAGE_INVENTORY = 1
    PAGE_SHELVES = 2

    def __init__(self):
        """Initialize Main Window."""
        super().__init__()

        # Core services
        self.theme = Theme(ThemeMode.LIGHT)
        self.inventory_manager = InventoryManager()
        self.image_manager = ImageManager()
        self.search_engine = SearchEngine()

        # Load data
        self.inventory_manager.load_data()
        self.search_engine.index_data(self.inventory_manager.medicines)

        # Track search dialog state
        self._search_dialog: Optional[SearchDialog] = None

        # Setup UI from generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Additional UI setup (logo, views, connections)
        self._setup_logo()
        self._setup_views()
        self._connect_signals()
        self._setup_shortcuts()

        # Apply theme & load data
        self.apply_theme()
        self.refresh_all()

        # Set default page
        self.navigate_to(self.PAGE_DASHBOARD, self.ui.btn_nav_dashboard)

        # Center window on screen
        self._center_on_screen()

    # ── UI Initialization (connecting generated UI to business logic) ──

    def _setup_logo(self):
        """Load and set the logo image on the sidebar."""
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "design-ui", "design-ui", "Qt_designer", "Logo.png"
        )
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            self.ui.logo_label.setPixmap(pixmap)
        else:
            self.ui.logo_label.setText("PHARMA.SYS")

    def _setup_views(self):
        """Create view widgets and add them to the stacked widget."""
        # Dashboard page
        self.dashboard = Dashboard(theme=self.theme)
        self.ui.stacked_main_content.addWidget(self.dashboard)

        # Inventory page
        self.inventory_view = InventoryView(theme=self.theme)
        self.ui.inv_layout.addWidget(self.inventory_view)
        self.ui.stacked_main_content.addWidget(self.ui.page_inventory)

        # Shelf page
        self.shelf_view = ShelfView(theme=self.theme)
        self.ui.shelf_layout.addWidget(self.shelf_view)
        self.ui.stacked_main_content.addWidget(self.ui.page_shelf)

    def _connect_signals(self):
        """Connect all signals to slots (business logic wiring)."""
        # Navigation buttons
        self.ui.btn_nav_dashboard.clicked.connect(
            lambda: self.navigate_to(self.PAGE_DASHBOARD, self.ui.btn_nav_dashboard)
        )
        self.ui.btn_nav_inventory.clicked.connect(
            lambda: self.navigate_to(self.PAGE_INVENTORY, self.ui.btn_nav_inventory)
        )
        self.ui.btn_nav_shelf.clicked.connect(
            lambda: self.navigate_to(self.PAGE_SHELVES, self.ui.btn_nav_shelf)
        )

        # Header buttons
        self.ui.btn_search.clicked.connect(self.show_search)
        self.ui.btn_toggle_theme.clicked.connect(self.toggle_theme)

        # Inventory view signals
        self.inventory_view.add_requested.connect(self.show_add_medicine)
        self.inventory_view.edit_requested.connect(self.show_edit_medicine)
        self.inventory_view.delete_requested.connect(self.delete_medicine)
        self.inventory_view.detail_requested.connect(self.show_medicine_detail)
        self.inventory_view.filter_requested.connect(self.show_filter_dialog)

        # Shelf view signals
        self.shelf_view.add_requested.connect(self.show_add_shelf)
        self.shelf_view.edit_requested.connect(self.show_edit_shelf)
        self.shelf_view.delete_requested.connect(self.delete_shelf)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        search_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        search_shortcut.activated.connect(self.show_search)

    def _center_on_screen(self):
        """Center the main window on the primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            self.move(window_geometry.topLeft())

    # ── Navigation ──

    def navigate_to(self, page_index: int, button: QPushButton):
        """
        Navigate to a page and update sidebar active state.

        Args:
            page_index: Page index
            button: The navigation button that was clicked
        """
        self.ui.stacked_main_content.setCurrentIndex(page_index)
        self.update_sidebar_active_state(button)

        titles = {
            self.PAGE_DASHBOARD: "Dashboard",
            self.PAGE_INVENTORY: "Danh sách thuốc",
            self.PAGE_SHELVES: "Quản lý kệ",
        }
        self.ui.page_title.setText(titles.get(page_index, ""))

    def update_sidebar_active_state(self, active_btn: QPushButton):
        """
        Update sidebar button styles based on which page is selected.

        Args:
            active_btn: The currently active navigation button
        """
        buttons = [
            self.ui.btn_nav_dashboard,
            self.ui.btn_nav_inventory,
            self.ui.btn_nav_shelf,
            self.ui.btn_nav_report,
            self.ui.btn_nav_setting,
        ]

        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                text-align: left;
                padding: 12px 20px;
                border: none;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #1E40AF; }
        """

        active_style = """
            QPushButton {
                background-color: #1E40AF;
                color: #FFFFFF;
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-left: 4px solid #6CC1FC;
                border-radius: 4px;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 16px;
                font-weight: bold;
            }
        """

        for btn in buttons:
            if btn == active_btn:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)

    def switch_page(self, index: int):
        """
        Switch to the specified page (for backward compat).

        Args:
            index: Page index
        """
        btn_map = {
            self.PAGE_DASHBOARD: self.ui.btn_nav_dashboard,
            self.PAGE_INVENTORY: self.ui.btn_nav_inventory,
            self.PAGE_SHELVES: self.ui.btn_nav_shelf,
        }
        btn = btn_map.get(index, self.ui.btn_nav_dashboard)
        self.navigate_to(index, btn)

    # ── Data Refresh ──

    def refresh_all(self):
        """Refresh all views with current data."""
        medicines = self.inventory_manager.get_all_medicines()
        shelves = self.inventory_manager.get_all_shelves()

        # Update search index
        self.search_engine.index_data(medicines)

        # Dashboard
        self.dashboard.load_data(medicines)

        # Inventory view
        self.inventory_view.load_medicines(medicines)

        # Shelf view — calculate used per shelf
        medicines_per_shelf = {}
        for med in medicines:
            medicines_per_shelf[med.shelf_id] = (
                medicines_per_shelf.get(med.shelf_id, 0) + med.quantity
            )
        self.shelf_view.load_shelves(shelves, medicines_per_shelf)

    # ── Medicine CRUD ──

    def show_add_medicine(self):
        """Show dialog to add a new medicine."""
        shelves = self.inventory_manager.get_all_shelves()

        dialog = MedicineDialog(
            parent=self,
            mode="add",
            shelves=shelves,
            image_manager=self.image_manager,
            theme=self.theme,
            remaining_capacity_func=self._get_shelf_remaining
        )

        if dialog.exec() == MedicineDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    # Handle image
                    image_path = ""
                    if "image_path" in data and data["image_path"]:
                        temp_image = data.pop("image_path")
                    else:
                        temp_image = None

                    medicine = Medicine(
                        id="",  # Auto-generate
                        name=data["name"],
                        quantity=data["quantity"],
                        expiry_date=data["expiry_date"],
                        shelf_id=data["shelf_id"],
                        price=data["price"],
                        image_path=""
                    )

                    added = self.inventory_manager.add_medicine(medicine)

                    # Save image with generated ID
                    if temp_image:
                        relative_path = self.image_manager.save_image(
                            temp_image, added.id
                        )
                        self.inventory_manager.update_medicine(
                            added.id,
                            {"image_path": relative_path}
                        )

                    self.refresh_all()

                    # Show success dialog
                    success = AddSuccessDialog(
                        self,
                        medicine_name=added.name,
                        medicine_id=added.id
                    )
                    success.exec()

                except ValueError as e:
                    if "sức chứa" in str(e).lower() or "capacity" in str(e).lower():
                        self._show_shelf_full_error(
                            data.get("shelf_id", ""),
                            str(e)
                        )
                    else:
                        QMessageBox.warning(
                            self, "Lỗi", str(e)
                        )

    def show_edit_medicine(self, medicine_id: str):
        """
        Show dialog to edit a medicine.

        Args:
            medicine_id: ID of medicine to edit
        """
        medicine = self.inventory_manager.get_medicine(medicine_id)
        if not medicine:
            QMessageBox.warning(
                self, "Lỗi",
                f"Không tìm thấy thuốc với mã '{medicine_id}'"
            )
            return

        shelves = self.inventory_manager.get_all_shelves()

        dialog = MedicineDialog(
            parent=self,
            mode="edit",
            medicine=medicine,
            shelves=shelves,
            image_manager=self.image_manager,
            theme=self.theme,
            remaining_capacity_func=self._get_shelf_remaining
        )

        if dialog.exec() == MedicineDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    # Handle image update
                    if "image_path" in data:
                        img_path = data["image_path"]
                        if img_path and not img_path.startswith("images"):
                            relative = self.image_manager.save_image(
                                img_path, medicine_id
                            )
                            data["image_path"] = relative

                    updated = self.inventory_manager.update_medicine(
                        medicine_id, data
                    )

                    # If shelf changed, ID changed — move image to new ID
                    if updated.id != medicine_id:
                        new_img_path = self.image_manager.rename_image(
                            medicine_id, updated.id
                        )
                        if new_img_path:
                            self.inventory_manager.update_medicine(
                                updated.id,
                                {"image_path": new_img_path}
                            )

                    self.refresh_all()

                    # Show success dialog with the updated ID
                    success = EditSuccessDialog(
                        self,
                        medicine_name=updated.name,
                        medicine_id=updated.id
                    )
                    success.exec()

                except ValueError as e:
                    if "sức chứa" in str(e).lower():
                        self._show_shelf_full_error(
                            data.get("shelf_id", ""),
                            str(e)
                        )
                    else:
                        QMessageBox.warning(
                            self, "Lỗi", str(e)
                        )

    def delete_medicine(self, medicine_id: str):
        """
        Delete a medicine after confirmation.

        Args:
            medicine_id: ID of medicine to delete
        """
        medicine = self.inventory_manager.get_medicine(medicine_id)
        if not medicine:
            return

        confirm = ConfirmDeleteDialog(
            self,
            medicine_name=medicine.name,
            medicine_id=medicine_id,
            quantity=medicine.quantity
        )

        if confirm.exec() == ConfirmDeleteDialog.DialogCode.Accepted:
            try:
                removed = self.inventory_manager.remove_medicine(medicine_id)
                self.image_manager.delete_image(medicine_id)
                self.refresh_all()

                success = DeleteSuccessDialog(
                    self,
                    medicine_name=removed.name,
                    medicine_id=medicine_id
                )
                success.exec()

            except ValueError as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    # ── Shelf CRUD ──

    def show_add_shelf(self):
        """Show dialog to add a new shelf."""
        dialog = ShelfDialog(
            parent=self,
            mode="add",
            theme=self.theme
        )

        if dialog.exec() == ShelfDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    shelf = Shelf(
                        id=data["id"],
                        zone=data["zone"],
                        column=data["column"],
                        row=data["row"],
                        capacity=data["capacity"]
                    )
                    self.inventory_manager.add_shelf(shelf)
                    self.refresh_all()

                    QMessageBox.information(
                        self, "Thành công",
                        f"Đã thêm kệ '{shelf.id}' thành công!"
                    )
                except ValueError as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def show_edit_shelf(self, shelf_id: str):
        """
        Show dialog to edit a shelf.

        Args:
            shelf_id: ID of shelf to edit
        """
        shelf = self.inventory_manager.get_shelf(shelf_id)
        if not shelf:
            QMessageBox.warning(
                self, "Lỗi",
                f"Không tìm thấy kệ '{shelf_id}'"
            )
            return

        dialog = ShelfDialog(
            parent=self,
            mode="edit",
            shelf=shelf,
            theme=self.theme
        )

        if dialog.exec() == ShelfDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data:
                try:
                    self.inventory_manager.update_shelf(
                        shelf_id,
                        {
                            "zone": data["zone"],
                            "column": data["column"],
                            "row": data["row"],
                            "capacity": data["capacity"],
                        }
                    )
                    self.refresh_all()

                    QMessageBox.information(
                        self, "Thành công",
                        f"Đã cập nhật kệ '{shelf_id}' thành công!"
                    )
                except ValueError as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def delete_shelf(self, shelf_id: str):
        """
        Delete a shelf after confirmation.

        Args:
            shelf_id: ID of shelf to delete
        """
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa kệ '{shelf_id}'?\n\n"
            "Thao tác này không thể hoàn tác.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_manager.remove_shelf(shelf_id)
                self.refresh_all()

                QMessageBox.information(
                    self, "Thành công",
                    f"Đã xóa kệ '{shelf_id}' thành công!"
                )
            except ValueError as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    # ── Search ──

    def show_search(self):
        """Show/toggle search dialog."""
        if self._search_dialog is not None:
            self._search_dialog._on_close()
            self._search_dialog = None
            return

        search = SearchDialog(
            parent=self,
            search_engine=self.search_engine,
            theme=self.theme
        )
        self._search_dialog = search

        result = search.exec()
        self._search_dialog = None

        if result == 1:  # Accepted
            if search.selected_medicine_id:
                self.navigate_to(self.PAGE_INVENTORY, self.ui.btn_nav_inventory)
                self.show_medicine_detail(search.selected_medicine_id)

    # ── Medicine Detail ──

    def show_medicine_detail(self, medicine_id: str):
        """
        Show read-only detail view for a medicine.

        Args:
            medicine_id: ID of medicine to view
        """
        medicine = self.inventory_manager.get_medicine(medicine_id)
        if not medicine:
            QMessageBox.warning(
                self, "Lỗi",
                f"Không tìm thấy thuốc với mã '{medicine_id}'"
            )
            return

        detail = MedicineDetailView(
            parent=self,
            medicine=medicine,
            image_manager=self.image_manager,
            theme=self.theme
        )
        detail.edit_requested.connect(self.show_edit_medicine)
        detail.delete_requested.connect(self.delete_medicine)
        detail.exec()

    # ── Filter ──

    def show_filter_dialog(self):
        """Show filter dialog for inventory."""
        shelves = self.inventory_manager.get_all_shelves()

        dialog = FilterMedicineDialog(
            parent=self,
            shelves=shelves,
            theme=self.theme
        )

        if dialog.exec() == FilterMedicineDialog.DialogCode.Accepted:
            filters = dialog.get_filters()
            self.inventory_view.set_filters(filters)

    # ── Theme ──

    def toggle_theme(self):
        """Toggle between Light and Dark modes."""
        new_mode = self.theme.toggle_mode()

        if new_mode == ThemeMode.DARK:
            self.ui.btn_toggle_theme.setText("☀️ Light")
        else:
            self.ui.btn_toggle_theme.setText("🌙 Dark")

        self.apply_theme()

        # Refresh charts with new theme colors
        self.dashboard.theme = self.theme
        self.dashboard.apply_theme()
        self.dashboard.update_charts()

        # Re-apply sidebar active state after theme change
        current_index = self.ui.stacked_main_content.currentIndex()
        btn_map = {
            self.PAGE_DASHBOARD: self.ui.btn_nav_dashboard,
            self.PAGE_INVENTORY: self.ui.btn_nav_inventory,
            self.PAGE_SHELVES: self.ui.btn_nav_shelf,
        }
        active_btn = btn_map.get(current_index, self.ui.btn_nav_dashboard)
        self.update_sidebar_active_state(active_btn)

    def apply_theme(self):
        """Apply current theme stylesheet to entire application."""
        app = QApplication.instance()
        if app:
            app.setStyleSheet(self.theme.get_stylesheet())

    # ── Helpers ──

    def _get_shelf_remaining(
        self, shelf_id: str, exclude_id: str = ""
    ) -> int:
        """
        Get remaining capacity of a shelf.

        Args:
            shelf_id: Shelf ID
            exclude_id: Medicine ID to exclude from used calculation

        Returns:
            Remaining capacity in units
        """
        return self.inventory_manager.get_shelf_remaining_capacity(
            shelf_id, exclude_id
        )

    def _show_shelf_full_error(self, shelf_id: str, message: str):
        """
        Show shelf full error dialog.

        Args:
            shelf_id: ID of the full shelf
            message: Error message with details
        """
        remaining = self.inventory_manager.get_shelf_remaining_capacity(
            shelf_id
        )
        dialog = ShelfFullErrorDialog(
            self,
            shelf_id=shelf_id,

            remaining_capacity=remaining
        )
        dialog.exec()

    # ── Close Event ──

    def closeEvent(self, event: QCloseEvent):
        """Show confirmation dialog before closing the application."""
        reply = QMessageBox.question(
            self,
            "Xác nhận thoát",
            "Bạn có chắc chắn muốn thoát chương trình?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()