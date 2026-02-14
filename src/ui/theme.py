"""
Theme system for Pharmacy Management System.

Implements Light and Dark mode based on design guidelines:
- Calm, professional color palette
- Proper contrast ratios
- Alert color system (Danger, Warning, Low Stock, Success)
"""
from enum import Enum
from typing import Dict


class ThemeMode(Enum):
    """Available theme modes."""
    LIGHT = "light"
    DARK = "dark"


class Theme:
    """
    Central theme system for the application.
    
    Provides:
    - Color palettes for Light and Dark modes
    - Alert color mappings
    - Typography settings
    - Spacing constants
    """
    
    # Spacing base unit (all spacing should be multiples of this)
    SPACING_BASE = 8
    
    # Border radius
    BORDER_RADIUS = 8
    
    # Component padding
    CARD_PADDING = 16
    DIALOG_PADDING = 24
    
    # Typography sizes
    FONT_SIZE_H1 = 20
    FONT_SIZE_H2 = 16
    FONT_SIZE_BODY = 14
    FONT_SIZE_TABLE = 13
    FONT_SIZE_CAPTION = 12
    FONT_SIZE_BUTTON = 14
    
    # Light Mode Colors
    LIGHT_COLORS = {
        # Neutral Foundation
        'background': '#F4F6F8',
        'surface': '#FFFFFF',
        'border': '#E0E6ED',
        'text_primary': '#2F3E46',
        'text_secondary': '#6C7A89',
        
        # Primary Action
        'primary': '#2E6F95',
        'primary_hover': '#255D7A',
        'primary_active': '#1F4E66',
        
        # Alert System - Danger (Expired/Out of Stock)
        'danger_text': '#C0392B',
        'danger_bg': '#FDECEA',
        
        # Alert System - Warning (Expiring Soon)
        'warning_text': '#D68910',
        'warning_bg': '#FFF4E5',
        
        # Alert System - Low Stock
        'low_stock_text': '#B9770E',
        'low_stock_bg': '#FEF9E7',
        
        # Alert System - Success
        'success_text': '#1E8449',
        'success_bg': '#E8F8F5',
        
        # Disabled state
        'disabled_bg': '#BDC3C7',
        'disabled_text': '#95A5A6',
    }
    
    # Dark Mode Colors
    DARK_COLORS = {
        # Base Colors
        'background': '#1F2933',
        'surface': '#273947',
        'border': '#3E4C59',
        'text_primary': '#E4E7EB',
        'text_secondary': '#9AA5B1',
        
        # Primary Action
        'primary': '#4FA3D1',
        'primary_hover': '#3C8DBC',
        'primary_active': '#2E6F95',
        
        # Alert System - Danger
        'danger_text': '#E74C3C',
        'danger_bg': '#3B1F1C',
        
        # Alert System - Warning
        'warning_text': '#F1C40F',
        'warning_bg': '#3D3314',
        
        # Alert System - Low Stock
        'low_stock_text': '#E67E22',
        'low_stock_bg': '#3B2A16',
        
        # Alert System - Success
        'success_text': '#2ECC71',
        'success_bg': '#1F3D2B',
        
        # Disabled state
        'disabled_bg': '#4B5D6B',
        'disabled_text': '#7B8794',
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
            /* Global Styles */
            QWidget {{
                font-family: "Segoe UI", "Arial", sans-serif;
                font-size: {self.FONT_SIZE_BODY}px;
                color: {c['text_primary']};
                background-color: {c['background']};
            }}
            
            /* Main Window */
            QMainWindow {{
                background-color: {c['background']};
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {c['primary']};
                color: #FFFFFF;
                border: none;
                border-radius: {self.BORDER_RADIUS}px;
                padding: {self.SPACING_BASE}px {self.SPACING_BASE * 2}px;
                font-size: {self.FONT_SIZE_BUTTON}px;
                font-weight: 500;
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
                background-color: transparent;
                color: {c['text_primary']};
                border: 2px solid {c['border']};
            }}
            
            QPushButton[secondary="true"]:hover {{
                border-color: {c['primary']};
                color: {c['primary']};
            }}
            
            /* Danger Buttons (Delete) */
            QPushButton[danger="true"] {{
                background-color: {c['danger_text']};
            }}
            
            QPushButton[danger="true"]:hover {{
                background-color: #A93226;
            }}
            
            /* Input Fields */
            QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: 2px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                padding: {self.SPACING_BASE}px;
                font-size: {self.FONT_SIZE_BODY}px;
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, 
            QDateEdit:focus, QComboBox:focus {{
                border-color: {c['primary']};
            }}
            
            QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
            QDateEdit:disabled, QComboBox:disabled {{
                background-color: {c['disabled_bg']};
                color: {c['disabled_text']};
            }}
            
            /* ComboBox Dropdown */
            QComboBox::drop-down {{
                border: none;
                padding-right: {self.SPACING_BASE}px;
            }}
            
            QComboBox::down-arrow {{
                image: url(down-arrow.png);
                width: 12px;
                height: 12px;
            }}
            
            /* Labels */
            QLabel {{
                color: {c['text_primary']};
                font-size: {self.FONT_SIZE_BODY}px;
            }}
            
            QLabel[secondary="true"] {{
                color: {c['text_secondary']};
                font-size: {self.FONT_SIZE_CAPTION}px;
            }}
            
            /* Tables */
            QTableView {{
                background-color: {c['surface']};
                alternate-background-color: {c['background']};
                border: 1px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                gridline-color: {c['border']};
                font-size: {self.FONT_SIZE_TABLE}px;
            }}
            
            QTableView::item {{
                padding: {self.SPACING_BASE}px;
            }}
            
            QTableView::item:selected {{
                background-color: {c['primary']};
                color: #FFFFFF;
            }}
            
            QHeaderView::section {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: none;
                border-bottom: 2px solid {c['border']};
                padding: {self.SPACING_BASE}px;
                font-weight: 600;
                font-size: {self.FONT_SIZE_TABLE}px;
            }}
            
            /* Dialogs */
            QDialog {{
                background-color: {c['surface']};
            }}
            
            /* Group Boxes */
            QGroupBox {{
                background-color: {c['surface']};
                border: 2px solid {c['border']};
                border-radius: {self.BORDER_RADIUS}px;
                margin-top: {self.SPACING_BASE * 2}px;
                padding: {self.CARD_PADDING}px;
                font-weight: 600;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 {self.SPACING_BASE}px;
                color: {c['text_primary']};
            }}
            
            /* Status Bar */
            QStatusBar {{
                background-color: {c['surface']};
                color: {c['text_secondary']};
                border-top: 1px solid {c['border']};
            }}
            
            /* Scroll Bars */
            QScrollBar:vertical {{
                background-color: {c['background']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {c['border']};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {c['text_secondary']};
            }}
            
            QScrollBar:horizontal {{
                background-color: {c['background']};
                height: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {c['border']};
                border-radius: 6px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {c['text_secondary']};
            }}
            
            /* List Widget (Sidebar) */
            QListWidget {{
                background-color: {c['surface']};
                border: none;
                outline: none;
            }}
            
            QListWidget::item {{
                padding: {self.SPACING_BASE * 2}px {self.SPACING_BASE}px;
                border-radius: {self.BORDER_RADIUS}px;
                margin: 4px;
            }}
            
            QListWidget::item:selected {{
                background-color: {c['primary']};
                color: #FFFFFF;
            }}
            
            QListWidget::item:hover {{
                background-color: {c['border']};
            }}
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
