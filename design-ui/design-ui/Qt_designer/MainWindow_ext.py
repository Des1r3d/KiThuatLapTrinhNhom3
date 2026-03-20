from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QTableWidgetItem

from PharmaSys import Ui_MainWindow

class MainWindow_ext(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.stacked_main_content.setContentsMargins(0, 0, 0, 0)

        # Biến trạng thái Theme
        self.is_dark_mode = False

        # Kết nối sự kiện nút Toggle Theme
        self.btn_toggle_theme.clicked.connect(self.switch_theme)

        # Kết nối Sidebar và khởi tạo trang mặc định
        self.setup_sidebar()

        # Áp dụng theme lần đầu
        self.apply_theme()


    def setup_sidebar(self):
        self.btn_nav_dashboard.clicked.connect(lambda: self.navigate_to(self.page_dashboard, self.btn_nav_dashboard))
        self.btn_nav_inventory.clicked.connect(lambda: self.navigate_to(self.page_inventory, self.btn_nav_inventory))
        self.btn_nav_shelf.clicked.connect(lambda: self.navigate_to(self.page_shelf, self.btn_nav_shelf))

        # Mặc định mở Dashboard
        self.navigate_to(self.page_dashboard, self.btn_nav_dashboard)

    #Hàm chuyển đổi page, tham số truyền: page được chuyển đến, button được bấm
    def navigate_to(self, page, button):
        self.stacked_main_content.setCurrentWidget(page)
        self.update_sidebar_active_state(button)

    #Hàm định dạng sidebar theo trang được chọn/không được chọn
    def update_sidebar_active_state(self, active_btn):
        # Cập nhật style cho các nút ở Sidebar theo Design System
        buttons = [self.btn_nav_dashboard, self.btn_nav_inventory, self.btn_nav_shelf, self.btn_nav_report, self.btn_nav_setting]

        # Nút KHÔNG CHỌN: Nền trong suốt, chữ trắng
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

        # Nút ĐANG CHỌN: Nền #1E40AF, Viền trái #6CC1FC
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

    def switch_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        app=QApplication.instance()
        if self.is_dark_mode:
            self.btn_toggle_theme.setText("☀️ Light")
            app.setStyleSheet(self.get_dark_qss())
        else:
            self.btn_toggle_theme.setText("🌙 Dark")
            app.setStyleSheet(self.get_light_qss())

    # ==========================================
    # BỘ MÃ MÀU LIGHT MODE TỪ DESIGN SYSTEM
    # ==========================================
    def get_light_qss(self):
        return """
            /* Font mặc định cho toàn bộ App */
            * { font-family: 'Segoe UI', 'Inter', sans-serif; }

            /* Nền tổng thể trang */
            QMainWindow, QStackedWidget, QWidget#page_dashboard, QWidget#page_inventory, QWidget#page_shelf, QDialog {
                background-color: #F4F6F8; 
            }

            /* Text nội dung chính */
            QLabel { color: #2F3E46; }

            /* ===== SIDEBAR ===== */
            QWidget#sidebar_container { background-color: #1C2944; border: none; }

            /* ===== FRAMES (Card, bảng, hộp thoại) ===== */
            QFrame#chart_row_container QFrame, QFrame#frame_expiring, QFrame#frame_low_stock, QWidget#frame_bar_chart, QWidget#frame_pie_chart {
                background-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 8px;
            }

            /* ===== NÚT BẤM ===== */
            /* Nút phụ / Hủy */
            QPushButton#btn_toggle_theme, QPushButton#btn_search, QPushButton#btn_filter {
                background-color: #F1F5F9;
                border: 1px solid #E0E6ED;
                border-radius: 6px;
                padding: 6px 16px;
                color: #2F3E46;
                font-weight: 600;
            }
            /* Nút chính / Lưu */
            QPushButton#btn_add_medicine, QPushButton#pushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton#btn_add_medicine:hover, QPushButton#pushButton:hover { background-color: #1E40AF; }

            /* ===== BẢNG DỮ LIỆU ===== */
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 8px;
                gridline-color: #E0E6ED;
                color: #2F3E46;
            }
            QHeaderView::section {
                background-color: #FFFFFF;
                color: #6C7A89; /* Text phụ */
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #E0E6ED;
                padding: 8px;
            }
            /* ===== DANH SÁCH CẢNH BÁO (LIST WIDGET) ===== */
            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 8px;
                color: #2F3E46;
                padding: 4px;
                outline: none; /* Bỏ viền chấm chấm khi click vào item */
            }
            /* Định dạng từng dòng cảnh báo bên trong */
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #F4F6F8; /* Đường kẻ mờ ngăn cách các cảnh báo */
            }
            /* Hiệu ứng khi lướt chuột qua cảnh báo */
            QListWidget::item:hover {
                background-color: #F1F5F9;
                border-radius: 6px;
            }
            /* Khi click chọn cảnh báo */
            QListWidget::item:selected {
                background-color: #E0E6ED;
                color: #2F3E46;
                border-radius: 6px;
            }
        """

    # ==========================================
    # BỘ MÃ MÀU DARK MODE TỪ DESIGN SYSTEM
    # ==========================================
    def get_dark_qss(self):
        return """
            * { font-family: 'Segoe UI', 'Inter', sans-serif; }

            /* Nền tổng thể trang */
            QMainWindow, QStackedWidget, QWidget#page_dashboard, QWidget#page_inventory, QWidget#page_shelf, QDialog {
                background-color: #1F2933; 
            }

            /* Text nội dung chính */
            QLabel { color: #E4E7EB; }

            /* ===== SIDEBAR (Không đổi màu theo thiết kế) ===== */
            QWidget#sidebar_container { background-color: #1C2944; border: none; }

            /* ===== FRAMES (Card, bảng, hộp thoại) ===== */
            QFrame#chart_row_container QFrame, QFrame#frame_expiring, QFrame#frame_low_stock, QWidget#frame_bar_chart, QWidget#frame_pie_chart {
                background-color: #273947;
                border: 1px solid #3E4C59;
                border-radius: 8px;
            }

            /* ===== NÚT BẤM ===== */
            /* Nút phụ / Hủy */
            QPushButton#btn_toggle_theme, QPushButton#btn_search, QPushButton#btn_filter {
                background-color: #1E3A5F;
                border: 1px solid #3E4C59;
                border-radius: 6px;
                padding: 6px 16px;
                color: #E4E7EB;
                font-weight: 600;
            }
            /* Nút chính / Lưu */
            QPushButton#btn_add_medicine, QPushButton#pushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton#btn_add_medicine:hover, QPushButton#pushButton:hover { background-color: #1E40AF; }

            /* ===== BẢNG DỮ LIỆU ===== */
            QTableWidget {
                background-color: #273947;
                border: 1px solid #3E4C59;
                border-radius: 8px;
                gridline-color: #3E4C59;
                color: #E4E7EB;
            }
            QHeaderView::section {
                background-color: #273947;
                color: #9AA5B1; /* Text phụ */
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #3E4C59;
                padding: 8px;
            }
            /* ===== DANH SÁCH CẢNH BÁO (LIST WIDGET) ===== */
            QListWidget {
                background-color: #273947;
                border: 1px solid #3E4C59;
                border-radius: 8px;
                color: #E4E7EB;
                padding: 4px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #1F2933; 
            }
            QListWidget::item:hover {
                background-color: #1E3A5F;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: #3E4C59;
                color: #E4E7EB;
                border-radius: 6px;
            }
        """

