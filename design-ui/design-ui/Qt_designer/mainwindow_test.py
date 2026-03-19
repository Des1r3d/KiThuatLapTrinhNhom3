import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt


class PharmaSysApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('PharmaSys.ui', self)

        self.stacked_main_content.setContentsMargins(0, 0, 0, 0)

        # Biến trạng thái Theme
        self.is_dark_mode = False

        # Kết nối sự kiện nút Toggle Theme
        self.btn_toggle_theme.clicked.connect(self.switch_theme)

        # Cấu hình màu sắc tĩnh cho KPI Cards theo Design System
        self.setup_kpi_cards()

        # Kết nối Sidebar và khởi tạo trang mặc định
        self.setup_sidebar()

        # Áp dụng theme lần đầu
        self.apply_theme()

    def setup_kpi_cards(self):
        # Dùng chung style cho các thẻ (Bo góc, chữ trắng, bỏ viền)
        base_style = """
            QFrame { border-radius: 8px; border: none; }
            QLabel { color: #FFFFFF; font-family: 'Segoe UI', 'Inter', sans-serif; background: transparent; }
        """
        # Áp dụng chính xác mã màu từ mục "Thẻ thống kê" trong Design System
        self.card_total.setStyleSheet("background-color: #3B82F6;" + base_style)
        self.card_expiring.setStyleSheet("background-color: #FF8800;" + base_style)
        self.card_expired.setStyleSheet("background-color: #EF4444;" + base_style)
        self.card_low_stock.setStyleSheet("background-color: #FFAD00;" + base_style)

    def setup_sidebar(self):
        self.btn_nav_dashboard.clicked.connect(lambda: self.navigate_to(self.page_dashboard, self.btn_nav_dashboard))
        self.btn_nav_inventory.clicked.connect(lambda: self.navigate_to(self.page_inventory, self.btn_nav_inventory))
        self.btn_nav_shelf.clicked.connect(lambda: self.navigate_to(self.page_shelf, self.btn_nav_shelf))

        # Mặc định mở Dashboard
        self.navigate_to(self.page_dashboard, self.btn_nav_dashboard)

    def navigate_to(self, page, button):
        self.stacked_main_content.setCurrentWidget(page)
        self.update_sidebar_active_state(button)

    def update_sidebar_active_state(self, active_btn):
        # Cập nhật style cho các nút ở Sidebar theo Design System
        buttons = [self.btn_nav_dashboard, self.btn_nav_inventory, self.btn_nav_shelf]

        # Nút KHÔNG CHỌN: Nền trong suốt, chữ trắng
        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                text-align: left;
                padding: 12px 20px;
                border: none;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 14px;
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
                font-size: 14px;
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
        if self.is_dark_mode:
            self.btn_toggle_theme.setText("☀️ Light")
            self.setStyleSheet(self.get_dark_qss())
        else:
            self.btn_toggle_theme.setText("🌙 Dark")
            self.setStyleSheet(self.get_light_qss())

    # ==========================================
    # BỘ MÃ MÀU LIGHT MODE TỪ DESIGN SYSTEM
    # ==========================================
    def get_light_qss(self):
        return """
            /* Font mặc định cho toàn bộ App */
            * { font-family: 'Segoe UI', 'Inter', sans-serif; }

            /* Nền tổng thể trang */
            QMainWindow, QStackedWidget, QWidget#page_dashboard, QWidget#page_inventory, QWidget#page_shelf {
                background-color: #F4F6F8; 
            }

            /* Text nội dung chính */
            QLabel { color: #2F3E46; }

            /* ===== SIDEBAR ===== */
            QWidget#sidebar_container { background-color: #1C2944; border: none; }

            /* ===== FRAMES (Card, bảng, hộp thoại) ===== */
            QFrame#chart_row_container QFrame, QFrame#frame_expiring, QFrame#frame_low_stock, QScrollArea {
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
        """

    # ==========================================
    # BỘ MÃ MÀU DARK MODE TỪ DESIGN SYSTEM
    # ==========================================
    def get_dark_qss(self):
        return """
            * { font-family: 'Segoe UI', 'Inter', sans-serif; }

            /* Nền tổng thể trang */
            QMainWindow, QStackedWidget, QWidget#page_dashboard, QWidget#page_inventory, QWidget#page_shelf {
                background-color: #1F2933; 
            }

            /* Text nội dung chính */
            QLabel { color: #E4E7EB; }

            /* ===== SIDEBAR (Không đổi màu theo thiết kế) ===== */
            QWidget#sidebar_container { background-color: #1C2944; border: none; }

            /* ===== FRAMES (Card, bảng, hộp thoại) ===== */
            QFrame#chart_row_container QFrame, QFrame#frame_expiring, QFrame#frame_low_stock, QScrollArea {
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
        """


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PharmaSysApp()
    window.show()
    sys.exit(app.exec())