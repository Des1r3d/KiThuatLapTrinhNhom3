"""
Hằng số cấu hình sidebar (cố định cho CẢ HAI chế độ, từ Qt_designer).
"""

SIDEBAR_BG = '#1C2944'
SIDEBAR_TEXT = '#FFFFFF'
SIDEBAR_ICON_INACTIVE = '#FFFFFF'
SIDEBAR_ACTIVE = '#1E40AF'
SIDEBAR_ACTIVE_ACCENT = '#6CC1FC'
SIDEBAR_LOGO_ACCENT = '#3B82F6'

# ── Style sheet cho nút sidebar ──

SIDEBAR_INACTIVE_STYLE = """
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

SIDEBAR_ACTIVE_STYLE = """
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
