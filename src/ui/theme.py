"""
Theme system for Pharmacy Management System — PHARMA.SYS Design System.

Implements Light and Dark mode based on PHARMA_SYS_Color_System.md:
- Primary Blue brand color (#2563EB)
- Dark sidebar (#0D1F3C) fixed for both modes
- Stat card colors (Blue, Yellow, Red, Green)
- Status badge system
- Inter font family
"""
from enum import Enum
from typing import Dict


class ThemeMode(Enum):
    """Available theme modes."""
    LIGHT = "light"
    DARK = "dark"


class Theme:
    """
    Central theme system for the application — PHARMA.SYS.

    Provides:
    - Color palettes for Light and Dark modes
    - Alert color mappings
    - Status badge colors
    - Stat card colors
    - Typography settings (Inter font)
    - Spacing constants (8px grid)
    """

    # ── Spacing (8px base grid) ──
    SPACING_BASE = 8

    # ── Border radius ──
    BORDER_RADIUS = 8
    BORDER_RADIUS_PILL = 10

    # ── Component padding ──
    CARD_PADDING = 16
    DIALOG_PADDING = 24

    # ── Typography ──
    FONT_FAMILY = '"Inter", "Segoe UI", "Roboto", sans-serif'
    FONT_SIZE_H1 = 20
    FONT_SIZE_H2 = 16
    FONT_SIZE_BODY = 14
    FONT_SIZE_TABLE = 13
    FONT_SIZE_CAPTION = 12
    FONT_SIZE_BUTTON = 14
    FONT_SIZE_BADGE = 11

    # ── Sidebar (fixed for BOTH modes) ──
    SIDEBAR_BG = '#0D1F3C'
    SIDEBAR_TEXT = '#FFFFFF'
    SIDEBAR_ICON_INACTIVE = '#94A3B8'
    SIDEBAR_ACTIVE = '#1E40AF'
    SIDEBAR_LOGO_ACCENT = '#3B82F6'

    # ── Stat Card backgrounds ──
    STAT_CARD_BLUE = '#3B82F6'
    STAT_CARD_YELLOW = '#F59E0B'
    STAT_CARD_RED = '#EF4444'
    STAT_CARD_GREEN = '#10B981'

    # ── Chart Colors ──
    CHART_BLUE = '#3B82F6'
    CHART_ORANGE = '#F59E0B'
    CHART_GREEN = '#10B981'
    CHART_RED = '#EF4444'

    # ── Light Mode Colors ──
    LIGHT_COLORS = {
        # Backgrounds
        'background': '#F0F2F5',
        'surface': '#FFFFFF',
        'table_row_alt': '#F8F9FB',

        # Borders
        'border': '#E2E8F0',

        # Text
        'text_primary': '#0F172A',
        'text_secondary': '#94A3B8',
        'text_heading': '#0F172A',
        'text_body': '#334155',
        'text_muted': '#94A3B8',
        'table_header_text': '#64748B',

        # Primary Action
        'primary': '#2563EB',
        'primary_hover': '#1E40AF',
        'primary_active': '#1D4ED8',

        # Forms / Inputs
        'input_bg': '#F9FAFB',
        'input_border': '#E2E8F0',
        'input_text': '#1E293B',
        'label_text': '#64748B',
        'cancel_btn_bg': '#F1F5F9',
        'save_btn_bg': '#2563EB',

        # Alert System — Danger (Expired / Critical)
        'danger_text': '#EF4444',
        'danger_bg': '#FEE2E2',

        # Alert System — Warning (Expiring Soon)
        'warning_text': '#F59E0B',
        'warning_bg': '#FEF3C7',

        # Alert System — Low Stock
        'low_stock_text': '#10B981',
        'low_stock_bg': '#D1FAE5',

        # Alert System — Success / In Stock / Normal
        'success_text': '#2563EB',
        'success_bg': '#DBEAFE',

        # Search bar
        'search_bg': '#FFFFFF',
        'search_border': '#E2E8F0',
        'search_icon': '#94A3B8',
        'search_highlight': '#EFF6FF',

        # Dialog overlay
        'overlay': 'rgba(0,0,0,0.4)',

        # Disabled state
        'disabled_bg': '#E2E8F0',
        'disabled_text': '#94A3B8',
    }

    # ── Dark Mode Colors ──
    DARK_COLORS = {
        # Backgrounds
        'background': '#0F1B2D',
        'surface': '#132237',
        'table_row_alt': '#1A2D45',

        # Borders
        'border': '#2D4A6A',

        # Text
        'text_primary': '#F1F5F9',
        'text_secondary': '#64748B',
        'text_heading': '#F1F5F9',
        'text_body': '#CBD5E1',
        'text_muted': '#64748B',
        'table_header_text': '#94A3B8',

        # Primary Action
        'primary': '#2563EB',
        'primary_hover': '#3B82F6',
        'primary_active': '#1D4ED8',

        # Forms / Inputs
        'input_bg': '#1E3A5F',
        'input_border': '#2D4A6A',
        'input_text': '#E2E8F0',
        'label_text': '#94A3B8',
        'cancel_btn_bg': '#1E3A5F',
        'save_btn_bg': '#2563EB',

        # Alert System — Danger
        'danger_text': '#EF4444',
        'danger_bg': '#7F1D1D',

        # Alert System — Warning
        'warning_text': '#F59E0B',
        'warning_bg': '#78350F',

        # Alert System — Low Stock
        'low_stock_text': '#10B981',
        'low_stock_bg': '#064E3B',

        # Alert System — Success / Normal
        'success_text': '#3B82F6',
        'success_bg': '#1E3A5F',

        # Search bar
        'search_bg': '#1A2D45',
        'search_border': '#2D4A6A',
        'search_icon': '#64748B',
        'search_highlight': '#1E3A5F',

        # Dialog overlay
        'overlay': 'rgba(0,0,0,0.6)',

        # Disabled state
        'disabled_bg': '#1A2D45',
        'disabled_text': '#64748B',
    }

    def __init__(self, mode: ThemeMode = ThemeMode.LIGHT):
        """
        Initialize theme with specified mode.

        Args:
            mode: ThemeMode.LIGHT or ThemeMode.DARK
        """
        self.mode = mode
        self._current_colors = (
            self.LIGHT_COLORS if mode == ThemeMode.LIGHT
            else self.DARK_COLORS
        )

    def get_color(self, key: str) -> str:
        """
        Get color value by key.

        Args:
            key: Color key (e.g., 'background', 'primary', 'danger_text')

        Returns:
            HEX color string
        """
        return self._current_colors.get(key, '#FFFFFF')

    def toggle_mode(self) -> ThemeMode:
        """
        Toggle between Light and Dark modes.

        Returns:
            New ThemeMode after toggle
        """
        self.mode = (
            ThemeMode.DARK if self.mode == ThemeMode.LIGHT
            else ThemeMode.LIGHT
        )
        self._current_colors = (
            self.LIGHT_COLORS if self.mode == ThemeMode.LIGHT
            else self.DARK_COLORS
        )
        return self.mode

    def set_mode(self, mode: ThemeMode) -> None:
        """
        Set specific theme mode.

        Args:
            mode: ThemeMode to apply
        """
        self.mode = mode
        self._current_colors = (
            self.LIGHT_COLORS if mode == ThemeMode.LIGHT
            else self.DARK_COLORS
        )

    def get_stylesheet(self) -> str:
        """
        Generate Qt stylesheet for current theme.

        Returns:
            Complete Qt StyleSheet string
        """
        c = self._current_colors

        return f"""
            /* ── Global ── */
            QWidget {{
                font-family: {self.FONT_FAMILY};
                font-size: {self.FONT_SIZE_BODY}px;
                color: {c['text_primary']};
                background-color: {c['background']};
            }}

            QMainWindow {{
                background-color: {c['background']};
            }}

            /* ── Buttons ── */
            QPushButton {{
                background-color: {c['primary']};
                color: #FFFFFF;
                border: none;
                border-radius: {self.BORDER_RADIUS}px;
                padding: {self.SPACING_BASE}px {self.SPACING_BASE * 2}px;
                font-size: {self.FONT_SIZE_BUTTON}px;
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

            /* Secondary Buttons */
            QPushButton[secondary="true"] {{
                background-color: {c['cancel_btn_bg']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
            }}

            QPushButton[secondary="true"]:hover {{
                border-color: {c['primary']};
                color: {c['primary']};
            }}

            /* Danger Buttons */
            QPushButton[danger="true"] {{
                background-color: {c['danger_text']};
            }}

            QPushButton[danger="true"]:hover {{
                background-color: #DC2626;
            }}

            /* ── Inputs ── */
            QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
                background-color: {c['input_bg']};
                color: {c['input_text']};
                border: 1px solid {c['input_border']};
                border-radius: {self.BORDER_RADIUS}px;
                padding: {self.SPACING_BASE}px {self.SPACING_BASE + 4}px;
                font-size: {self.FONT_SIZE_BODY}px;
                min-height: 28px;
            }}

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
            QDateEdit:focus, QComboBox:focus {{
                border-color: {c['primary']};
                border-width: 2px;
            }}

            QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
            QDateEdit:disabled, QComboBox:disabled {{
                background-color: {c['disabled_bg']};
                color: {c['disabled_text']};
            }}

            /* ComboBox */
            QComboBox::drop-down {{
                border: none;
                padding-right: {self.SPACING_BASE}px;
            }}

            QComboBox QAbstractItemView {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
                selection-background-color: {c['primary']};
                selection-color: #FFFFFF;
            }}

            /* ── Labels ── */
            QLabel {{
                color: {c['text_primary']};
                font-size: {self.FONT_SIZE_BODY}px;
                background-color: transparent;
            }}

            QLabel[secondary="true"] {{
                color: {c['text_secondary']};
                font-size: {self.FONT_SIZE_CAPTION}px;
            }}

            /* ── Tables ── */
            QTableWidget, QTableView {{
                background-color: {c['surface']};
                alternate-background-color: {c['table_row_alt']};
                border: 1px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                gridline-color: {c['border']};
                font-size: {self.FONT_SIZE_TABLE}px;
            }}

            QTableWidget::item, QTableView::item {{
                padding: {self.SPACING_BASE}px;
                border-bottom: 1px solid {c['border']};
            }}

            QTableWidget::item:selected, QTableView::item:selected {{
                background-color: {c['primary']};
                color: #FFFFFF;
            }}

            QHeaderView::section {{
                background-color: {c['surface']};
                color: {c['table_header_text']};
                border: none;
                border-bottom: 2px solid {c['border']};
                padding: {self.SPACING_BASE + 2}px {self.SPACING_BASE}px;
                font-weight: 600;
                font-size: {self.FONT_SIZE_TABLE}px;
                text-transform: uppercase;
            }}

            /* ── Dialogs ── */
            QDialog {{
                background-color: {c['surface']};
            }}

            /* ── Group Boxes ── */
            QGroupBox {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                margin-top: {self.SPACING_BASE * 2}px;
                padding: {self.CARD_PADDING}px;
                padding-top: {self.CARD_PADDING + 8}px;
                font-weight: 600;
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 {self.SPACING_BASE}px;
                color: {c['text_primary']};
            }}

            /* ── Status Bar ── */
            QStatusBar {{
                background-color: {c['surface']};
                color: {c['text_secondary']};
                border-top: 1px solid {c['border']};
                font-size: {self.FONT_SIZE_CAPTION}px;
                padding: 4px {self.SPACING_BASE}px;
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

            /* ── Sidebar ── */
            QFrame#sidebar {{
                background-color: {self.SIDEBAR_BG};
                border: none;
                border-right: 1px solid #1A2D45;
            }}

            QFrame#sidebar QLabel {{
                color: {self.SIDEBAR_TEXT};
                background-color: transparent;
            }}

            QFrame#sidebar QLabel#logo_label {{
                color: {self.SIDEBAR_LOGO_ACCENT};
                font-size: 18px;
                font-weight: 700;
            }}

            QFrame#sidebar QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
                color: {self.SIDEBAR_TEXT};
            }}

            QFrame#sidebar QListWidget::item {{
                padding: 12px 16px;
                border-radius: {self.BORDER_RADIUS}px;
                margin: 2px 8px;
                color: {self.SIDEBAR_ICON_INACTIVE};
                font-size: {self.FONT_SIZE_BODY}px;
            }}

            QFrame#sidebar QListWidget::item:selected {{
                background-color: {self.SIDEBAR_ACTIVE};
                color: {self.SIDEBAR_TEXT};
                font-weight: 600;
            }}

            QFrame#sidebar QListWidget::item:hover:!selected {{
                background-color: rgba(255, 255, 255, 0.08);
                color: {self.SIDEBAR_TEXT};
            }}

            QFrame#sidebar QPushButton {{
                background-color: transparent;
                color: {self.SIDEBAR_ICON_INACTIVE};
                border: 1px solid rgba(255, 255, 255, 0.15);
                font-size: {self.FONT_SIZE_CAPTION}px;
                padding: 8px 12px;
            }}

            QFrame#sidebar QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.08);
                color: {self.SIDEBAR_TEXT};
            }}

            /* ── Top Bar ── */
            QFrame#topbar {{
                background-color: {c['surface']};
                border-bottom: 1px solid {c['border']};
            }}

            QFrame#topbar QLabel {{
                background-color: transparent;
            }}

            QFrame#topbar QPushButton {{
                min-height: 28px;
                padding: 6px 14px;
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
            }}

            QMessageBox QLabel {{
                color: {c['text_primary']};
            }}

            /* ── Menu ── */
            QMenu {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                padding: 4px;
            }}

            QMenu::item {{
                padding: 8px 24px;
                border-radius: 4px;
            }}

            QMenu::item:selected {{
                background-color: {c['primary']};
                color: #FFFFFF;
            }}
        """

    def get_sidebar_stylesheet(self) -> str:
        """
        Get sidebar-specific stylesheet (dark background for both modes).

        Returns:
            Sidebar-specific stylesheet string
        """
        return f"""
            background-color: {self.SIDEBAR_BG};
            color: {self.SIDEBAR_TEXT};
        """

    def get_alert_colors(self, alert_type: str) -> Dict[str, str]:
        """
        Get colors for specific alert type.

        Args:
            alert_type: One of 'danger', 'warning', 'low_stock', 'success'

        Returns:
            Dictionary with 'text' and 'bg' color keys
        """
        c = self._current_colors

        alert_map = {
            'danger': {
                'text': c['danger_text'],
                'bg': c['danger_bg']
            },
            'warning': {
                'text': c['warning_text'],
                'bg': c['warning_bg']
            },
            'low_stock': {
                'text': c['low_stock_text'],
                'bg': c['low_stock_bg']
            },
            'success': {
                'text': c['success_text'],
                'bg': c['success_bg']
            }
        }

        return alert_map.get(alert_type, {'text': c['text_primary'], 'bg': c['background']})

    def get_stat_card_style(self, card_type: str) -> str:
        """
        Get stylesheet for stat cards on the dashboard.

        Args:
            card_type: One of 'total', 'expiring', 'expired', 'low_stock'

        Returns:
            Inline stylesheet string for the card
        """
        color_map = {
            'total': self.STAT_CARD_BLUE,
            'expiring': self.STAT_CARD_YELLOW,
            'expired': self.STAT_CARD_RED,
            'low_stock': self.STAT_CARD_GREEN,
        }
        bg = color_map.get(card_type, self.STAT_CARD_BLUE)

        return (
            f"background-color: {bg}; "
            f"color: #FFFFFF; "
            f"border-radius: {self.BORDER_RADIUS}px; "
            f"border: none; "
            f"border-bottom: 4px solid rgba(0,0,0,0.15);"
        )

    def get_badge_style(self, status_type: str) -> str:
        """
        Get stylesheet for status badge (pill shape).

        Args:
            status_type: One of 'danger', 'warning', 'low_stock', 'success'

        Returns:
            Inline stylesheet string for the badge
        """
        colors = self.get_alert_colors(status_type)

        return (
            f"background-color: {colors['bg']}; "
            f"color: {colors['text']}; "
            f"padding: 4px 10px; "
            f"border-radius: {self.BORDER_RADIUS_PILL}px; "
            f"font-size: {self.FONT_SIZE_BADGE}px; "
            f"font-weight: 700;"
        )
