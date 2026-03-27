"""
Các hàm trợ giúp màu huy hiệu trạng thái và cảnh báo — Hệ thống Thiết kế PHARMA.SYS.
"""
from src.ui.theme.tokens import BORDER_RADIUS, BORDER_RADIUS_PILL, FONT_SIZE_BADGE
from src.ui.theme.cards import STAT_CARD_BLUE, STAT_CARD_YELLOW, STAT_CARD_RED, STAT_CARD_GREEN


def get_alert_colors(current_colors: dict, alert_type: str) -> dict:
    """
    Lấy màu cho loại cảnh báo cụ thể.

    Tham số:
        current_colors: Dictionary bảng màu đang sử dụng.
        alert_type: Một trong 'danger', 'warning', 'low_stock', 'success'.

    Trả về:
        Dictionary với các khóa 'text' và 'bg'.
    """
    c = current_colors
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


def get_stat_card_style(card_type: str) -> str:
    """
    Lấy stylesheet cho thẻ thống kê trên dashboard.

    Tham số:
        card_type: Một trong 'total', 'expiring', 'expired', 'low_stock'.

    Trả về:
        Chuỗi stylesheet inline cho thẻ.
    """
    color_map = {
        'total': STAT_CARD_BLUE,
        'expiring': STAT_CARD_YELLOW,
        'expired': STAT_CARD_RED,
        'low_stock': STAT_CARD_GREEN,
    }
    bg = color_map.get(card_type, STAT_CARD_BLUE)

    return (
        f"background-color: {bg}; "
        f"color: #FFFFFF; "
        f"border-radius: {BORDER_RADIUS}px; "
        f"border: none; "
        f"border-bottom: 4px solid rgba(0,0,0,0.15);"
    )


def get_badge_style(current_colors: dict, status_type: str) -> str:
    """
    Lấy stylesheet cho huy hiệu trạng thái (dạng viên).

    Tham số:
        current_colors: Dictionary bảng màu đang sử dụng.
        status_type: Một trong 'danger', 'warning', 'low_stock', 'success'.

    Trả về:
        Chuỗi stylesheet inline cho huy hiệu.
    """
    colors = get_alert_colors(current_colors, status_type)

    return (
        f"background-color: {colors['bg']}; "
        f"color: {colors['text']}; "
        f"padding: 4px 10px; "
        f"border-radius: {BORDER_RADIUS_PILL}px; "
        f"font-size: {FONT_SIZE_BADGE}px; "
        f"font-weight: 700;"
    )
