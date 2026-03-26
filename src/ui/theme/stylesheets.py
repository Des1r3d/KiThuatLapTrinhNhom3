"""
Các hàm tạo stylesheet Qt cho chế độ Sáng/Tối — Hệ thống Thiết kế PHARMA.SYS.
"""
from src.ui.theme import tokens
from src.ui.theme import sidebar as sb


def get_stylesheet(colors: dict) -> str:
    """
    Tạo stylesheet Qt đầy đủ cho bảng màu đã cho.

    Tham số:
        colors: Dictionary bảng màu (LIGHT_COLORS hoặc DARK_COLORS).

    Trả về:
        Chuỗi Qt StyleSheet hoàn chỉnh.
    """
    c = colors

    return f"""
        /* ── Global ── */
        * {{
            font-family: {tokens.FONT_FAMILY};
        }}

        /* Nền tổng thể trang */
        QMainWindow, QStackedWidget, QWidget#page_dashboard, QWidget#page_inventory, QWidget#page_shelf, QDialog {{
            background-color: {c['background']};
        }}

        /* Text nội dung chính */
        QLabel {{
            color: {c['text_primary']};
        }}

        /* ── Buttons ── */
        /* Nút phụ / Hủy */
        QPushButton#btn_toggle_theme, QPushButton#btn_search, QPushButton#btn_filter {{
            background-color: {c['cancel_btn_bg']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 6px 16px;
            color: {c['text_primary']};
            font-weight: 600;
        }}

        /* Nút chính / Lưu */
        QPushButton#btn_add_medicine, QPushButton#pushButton {{
            background-color: {c['primary']};
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 6px 16px;
            font-weight: 600;
        }}
        QPushButton#btn_add_medicine:hover, QPushButton#pushButton:hover {{
            background-color: {c['primary_hover']};
        }}

        /* Generic button defaults */
        QPushButton {{
            background-color: {c['primary']};
            color: #FFFFFF;
            border: none;
            border-radius: {tokens.BORDER_RADIUS}px;
            padding: {tokens.SPACING_BASE}px {tokens.SPACING_BASE * 2}px;
            font-size: {tokens.FONT_SIZE_BUTTON}px;
            font-weight: 600;
            min-height: 32px;
        }}

        QPushButton:hover {{
            background-color: {c['primary_hover']};
        }}

        QPushButton:pressed {{
            background-color: {c['primary_active']};
        }}

        QPushButton:disabled {{
            background-color: {c['disabled_bg']};
            color: {c['disabled_text']};
        }}

        /* ── Sidebar (from Qt_designer design system) ── */
        QWidget#sidebar_container {{
            background-color: {sb.SIDEBAR_BG};
            border: none;
        }}

        QWidget#sidebar_container QLabel {{
            color: {sb.SIDEBAR_TEXT};
            background-color: transparent;
        }}

        /* ── FRAMES (Card, bảng, hộp thoại) ── */
        QFrame#chart_row_container QFrame, QFrame#frame_expiring, QFrame#frame_low_stock, QWidget#frame_bar_chart, QWidget#frame_pie_chart {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: 8px;
        }}

        /* ── BẢNG DỮ LIỆU ── */
        QTableWidget {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            gridline-color: {c['border']};
            color: {c['text_primary']};
            alternate-background-color: {c['table_row_alt']};
        }}
        QTableWidget::item:selected {{
            background-color: {c['table_selection_bg']};
            color: {c['table_selection_text']};
        }}
        QTableWidget::item:hover:!selected {{
            background-color: {c['table_hover_bg']};
        }}
        QHeaderView::section {{
            background-color: {c['surface']};
            color: {c['text_secondary']};
            font-weight: bold;
            border: none;
            border-bottom: 1px solid {c['border']};
            padding: 8px;
        }}

        /* ── DANH SÁCH CẢNH BÁO (LIST WIDGET) ── */
        QListWidget {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            color: {c['text_primary']};
            padding: 4px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {c['background']};
        }}
        QListWidget::item:hover {{
            background-color: {c['cancel_btn_bg']};
            border-radius: 6px;
        }}
        QListWidget::item:selected {{
            background-color: {c['border']};
            color: {c['text_primary']};
            border-radius: 6px;
        }}

        /* ── Scroll Area ── */
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}

        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}

        /* ── Message Box ── */
        QMessageBox {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {tokens.BORDER_RADIUS + 4}px;
        }}

        QMessageBox QLabel {{
            color: {c['text_primary']};
            font-size: {tokens.FONT_SIZE_BODY}px;
            padding: 8px 4px;
        }}

        QMessageBox QPushButton {{
            min-width: 90px;
            min-height: 34px;
            padding: 8px 20px;
            border-radius: {tokens.BORDER_RADIUS}px;
        }}

        /* ── Calendar Widget (for QDateEdit) ── */
        QCalendarWidget {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
        }}

        QCalendarWidget QAbstractItemView {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            selection-background-color: {c['primary']};
            selection-color: #FFFFFF;
            alternate-background-color: {c['table_row_alt']};
        }}

        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: {c['primary']};
            color: #FFFFFF;
        }}

        QCalendarWidget QToolButton {{
            background-color: transparent;
            color: #FFFFFF;
            font-weight: bold;
            padding: 4px 8px;
        }}

        QCalendarWidget QToolButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }}

        /* ── Menu ── */
        QMenu {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {tokens.BORDER_RADIUS}px;
            padding: 4px;
        }}

        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
            color: {c['text_primary']};
        }}

        QMenu::item:selected {{
            background-color: {c['primary']};
            color: #FFFFFF;
        }}

        /* ── Inputs ── */
        QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
            background-color: {c['input_bg']};
            color: {c['input_text']};
            border: 1px solid {c['input_border']};
            border-radius: {tokens.BORDER_RADIUS}px;
            padding: {tokens.SPACING_BASE}px {tokens.SPACING_BASE + 4}px;
            font-size: {tokens.FONT_SIZE_BODY}px;
            min-height: 28px;
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
        QDateEdit:focus, QComboBox:focus {{
            border-color: {c['primary']};
            border-width: 2px;
        }}

        /* ComboBox */
        QComboBox::drop-down {{
            border: none;
            padding-right: {tokens.SPACING_BASE}px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            selection-background-color: {c['primary']};
            selection-color: #FFFFFF;
        }}

        /* ── Dialogs ── */
        QDialog {{
            background-color: {c['surface']};
        }}

        /* ── Group Boxes ── */
        QGroupBox {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {tokens.BORDER_RADIUS}px;
            margin-top: {tokens.SPACING_BASE * 2}px;
            padding: {tokens.CARD_PADDING}px;
            padding-top: {tokens.CARD_PADDING + 8}px;
            font-weight: 600;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 {tokens.SPACING_BASE}px;
            color: {c['text_primary']};
        }}

        /* ── Scroll Bars ── */
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            border-radius: 4px;
            margin: 2px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {c['border']};
            border-radius: 4px;
            min-height: 24px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {c['text_secondary']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: transparent;
            height: 8px;
            border-radius: 4px;
            margin: 2px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {c['border']};
            border-radius: 4px;
            min-width: 24px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {c['text_secondary']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* ── Scroll Area ── */
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}

        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}

        /* ── Message Box ── */
        QMessageBox {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {tokens.BORDER_RADIUS + 4}px;
        }}

        QMessageBox QLabel {{
            color: {c['text_primary']};
            font-size: {tokens.FONT_SIZE_BODY}px;
            padding: 8px 4px;
        }}

        QMessageBox QPushButton {{
            min-width: 90px;
            min-height: 34px;
            padding: 8px 20px;
            border-radius: {tokens.BORDER_RADIUS}px;
        }}

        /* ── Calendar Widget (for QDateEdit) ── */
        QCalendarWidget {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
        }}

        QCalendarWidget QAbstractItemView {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            selection-background-color: {c['primary']};
            selection-color: #FFFFFF;
            alternate-background-color: {c['table_row_alt']};
        }}

        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: {c['primary']};
            color: #FFFFFF;
        }}

        QCalendarWidget QToolButton {{
            background-color: transparent;
            color: #FFFFFF;
            font-weight: bold;
            padding: 4px 8px;
        }}

        QCalendarWidget QToolButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }}

        /* ── Danger Buttons ── */
        QPushButton[danger="true"] {{
            background-color: {c['danger_text']};
        }}

        QPushButton[danger="true"]:hover {{
            background-color: #DC2626;
        }}

        QPushButton[danger="true"]:pressed {{
            background-color: #B91C1C;
        }}
    """


def get_sidebar_stylesheet() -> str:
    """
    Lấy stylesheet riêng cho sidebar (nền tối cho cả hai chế độ).

    Trả về:
        Chuỗi stylesheet cho sidebar.
    """
    return f"""
        background-color: {sb.SIDEBAR_BG};
        color: {sb.SIDEBAR_TEXT};
    """
