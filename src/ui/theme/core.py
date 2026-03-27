"""
Lớp Theme cốt lõi và enum ThemeMode — Hệ thống Thiết kế PHARMA.SYS.
"""
from enum import Enum
from typing import Dict

from src.ui.theme.colors import LIGHT_COLORS, DARK_COLORS
from src.ui.theme.stylesheets import get_stylesheet, get_sidebar_stylesheet
from src.ui.theme.badges import get_alert_colors, get_stat_card_style, get_badge_style
from src.ui.theme import tokens, sidebar, cards


class ThemeMode(Enum):
    """Các chế độ chủ đề có sẵn."""
    LIGHT = "light"
    DARK = "dark"


class Theme:
    """
    Hệ thống chủ đề trung tâm cho ứng dụng — PHARMA.SYS.

    Cung cấp:
    - Bảng màu cho chế độ Sáng và Tối
    - Ánh xạ màu cảnh báo
    - Màu huy hiệu trạng thái
    - Màu thẻ thống kê
    - Cài đặt kiểu chữ (Segoe UI / Inter)
    - Hằng số khoảng cách (lưới 8px)
    """

    # ── Xuất token dưới dạng thuộc tính lớp để tương thích ngược ──
    SPACING_BASE = tokens.SPACING_BASE
    BORDER_RADIUS = tokens.BORDER_RADIUS
    BORDER_RADIUS_PILL = tokens.BORDER_RADIUS_PILL
    CARD_PADDING = tokens.CARD_PADDING
    DIALOG_PADDING = tokens.DIALOG_PADDING

    FONT_FAMILY = tokens.FONT_FAMILY
    FONT_SIZE_H1 = tokens.FONT_SIZE_H1
    FONT_SIZE_H2 = tokens.FONT_SIZE_H2
    FONT_SIZE_BODY = tokens.FONT_SIZE_BODY
    FONT_SIZE_TABLE = tokens.FONT_SIZE_TABLE
    FONT_SIZE_CAPTION = tokens.FONT_SIZE_CAPTION
    FONT_SIZE_BUTTON = tokens.FONT_SIZE_BUTTON
    FONT_SIZE_BADGE = tokens.FONT_SIZE_BADGE

    SIDEBAR_BG = sidebar.SIDEBAR_BG
    SIDEBAR_TEXT = sidebar.SIDEBAR_TEXT
    SIDEBAR_ICON_INACTIVE = sidebar.SIDEBAR_ICON_INACTIVE
    SIDEBAR_ACTIVE = sidebar.SIDEBAR_ACTIVE
    SIDEBAR_ACTIVE_ACCENT = sidebar.SIDEBAR_ACTIVE_ACCENT
    SIDEBAR_LOGO_ACCENT = sidebar.SIDEBAR_LOGO_ACCENT

    STAT_CARD_BLUE = cards.STAT_CARD_BLUE
    STAT_CARD_YELLOW = cards.STAT_CARD_YELLOW
    STAT_CARD_RED = cards.STAT_CARD_RED
    STAT_CARD_GREEN = cards.STAT_CARD_GREEN

    CHART_BLUE = cards.CHART_BLUE
    CHART_ORANGE = cards.CHART_ORANGE
    CHART_GREEN = cards.CHART_GREEN
    CHART_RED = cards.CHART_RED

    # Bảng màu gốc (cấp lớp)
    LIGHT_COLORS = LIGHT_COLORS
    DARK_COLORS = DARK_COLORS

    def __init__(self, mode: ThemeMode = ThemeMode.LIGHT):
        """
        Khởi tạo chủ đề với chế độ chỉ định.

        Tham số:
            mode: ThemeMode.LIGHT hoặc ThemeMode.DARK
        """
        self.mode = mode
        self._current_colors = (
            self.LIGHT_COLORS if mode == ThemeMode.LIGHT
            else self.DARK_COLORS
        )

    def get_color(self, key: str) -> str:
        """
        Lấy giá trị màu theo khóa.

        Tham số:
            key: Khóa màu (VD: 'background', 'primary', 'danger_text')

        Trả về:
            Chuỗi màu HEX
        """
        return self._current_colors.get(key, '#FFFFFF')

    def toggle_mode(self) -> ThemeMode:
        """
        Chuyển đổi giữa chế độ Sáng và Tối.

        Trả về:
            ThemeMode mới sau khi chuyển đổi
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
        Đặt chế độ chủ đề cụ thể.

        Tham số:
            mode: ThemeMode cần áp dụng
        """
        self.mode = mode
        self._current_colors = (
            self.LIGHT_COLORS if mode == ThemeMode.LIGHT
            else self.DARK_COLORS
        )

    def get_stylesheet(self) -> str:
        """Tạo stylesheet Qt cho chủ đề hiện tại."""
        return get_stylesheet(self._current_colors)

    def get_sidebar_stylesheet(self) -> str:
        """Lấy stylesheet riêng cho sidebar."""
        return get_sidebar_stylesheet()

    def get_alert_colors(self, alert_type: str) -> Dict[str, str]:
        """Lấy màu cho loại cảnh báo cụ thể."""
        return get_alert_colors(self._current_colors, alert_type)

    def get_stat_card_style(self, card_type: str) -> str:
        """Lấy stylesheet cho thẻ thống kê trên dashboard."""
        return get_stat_card_style(card_type)

    def get_badge_style(self, status_type: str) -> str:
        """Lấy stylesheet cho huy hiệu trạng thái (dạng viên)."""
        return get_badge_style(self._current_colors, status_type)
