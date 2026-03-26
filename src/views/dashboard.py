"""
Dashboard — Giao diện Thống kê và Biểu đồ PHARMA.SYS.

File này CHỈ chứa mã giao diện (UI).
Logic xử lý dữ liệu nằm trong src/dashboard_manager.py.

Tính năng:
- 4 thẻ KPI màu (Tổng, Sắp hết hạn, Hết hạn, Tồn kho thấp)
- Biểu đồ tròn (donut) phân bố hạn sử dụng
- Biểu đồ cột top thuốc theo số lượng
- Bảng cảnh báo thuốc sắp hết hạn
- Bảng cảnh báo thuốc tồn kho thấp
"""
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.models import Medicine
from src.dashboard_manager import (
    DashboardManager, DashboardStats,
    PieChartData, BarChartData,
    ExpiryItem, LowStockItem
)
from src.ui.theme import Theme


class StatCard(QFrame):
    """
    Widget thẻ KPI với nền màu.

    Mỗi thẻ hiển thị số, nhãn, icon và phụ đề tùy chọn.
    Màu nền được xác định bởi card_type.
    """

    def __init__(
        self,
        title: str,
        value: int,
        icon: str = "",
        subtitle: str = "",
        card_type: str = "total",
        theme: Optional[Theme] = None,
        parent=None
    ):
        """
        Khởi tạo thẻ thống kê.

        Tham số:
            title: Tiêu đề thẻ
            value: Giá trị thống kê hiển thị
            icon: Icon emoji
            subtitle: Phụ đề mô tả
            card_type: 'total', 'expiring', 'expired', 'low_stock'
            theme: Thực thể Theme
            parent: Widget cha
        """
        super().__init__(parent)

        self.theme = theme or Theme()
        self.card_type = card_type

        self._setup_ui(title, value, icon, subtitle)

    def _setup_ui(self, title: str, value: int, icon: str, subtitle: str):
        """Thiết lập giao diện thẻ."""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.CARD_PADDING + 4,
            Theme.CARD_PADDING,
            Theme.CARD_PADDING + 4,
            Theme.CARD_PADDING
        )
        layout.setSpacing(4)

        # Hàng trên: tiêu đề + icon
        top_row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: rgba(255,255,255,0.85); font-size: 13px; "
            "font-weight: 500; background: transparent;"
        )
        top_row.addWidget(title_label)
        top_row.addStretch()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(
            "font-size: 20px; background: transparent; "
            "color: rgba(255,255,255,0.7);"
        )
        top_row.addWidget(icon_label)
        layout.addLayout(top_row)

        # Giá trị
        self.value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(32)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(
            "color: #FFFFFF; background: transparent;"
        )
        layout.addWidget(self.value_label)

        # Phụ đề
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 12px; "
            "background: transparent;"
        )
        layout.addWidget(self.subtitle_label)

        self.setLayout(layout)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(120)

        # Áp dụng màu thẻ
        self.setStyleSheet(self.theme.get_stat_card_style(self.card_type))

    def update_value(self, value: int, subtitle: str = ""):
        """Cập nhật giá trị và phụ đề hiển thị."""
        self.value_label.setText(str(value))
        if subtitle:
            self.subtitle_label.setText(subtitle)


class Dashboard(QWidget):
    """
    Widget Dashboard với thẻ KPI, biểu đồ và bảng cảnh báo.

    CHỈ chứa mã giao diện. Mọi logic xử lý dữ liệu được
    ủy quyền cho DashboardManager (src/dashboard_manager.py).

    Tính năng:
    - 4 thẻ thống kê tổng quan màu sắc
    - Biểu đồ tròn phân bố hạn sử dụng
    - Biểu đồ cột top 10 thuốc theo số lượng
    - Bảng cảnh báo nhanh (sắp hết hạn, tồn kho thấp)
    """

    def __init__(self, parent=None, theme: Optional[Theme] = None):
        """
        Khởi tạo Dashboard.

        Tham số:
            parent: Widget cha
            theme: Thực thể Theme cho kiểu dáng
        """
        super().__init__(parent)

        self.theme = theme or Theme()
        self.manager = DashboardManager()

        self._setup_ui()
        self._apply_theme()

    def _setup_ui(self):
        """Thiết lập các thành phần giao diện Dashboard."""
        # Vùng cuộn chính
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Widget chính
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(Theme.SPACING_BASE * 3)
        layout.setContentsMargins(
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 2,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3
        )

        # ── 4 Thẻ KPI ──
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(Theme.SPACING_BASE * 2)

        self.total_card = StatCard(
            "Tổng tồn kho", 0, "",
            "", "total", self.theme
        )
        self.expiring_card = StatCard(
            "Sắp hết hạn", 0, "",
            "Cần xử lý", "expiring", self.theme
        )
        self.expired_card = StatCard(
            "Hết hạn", 0, "",
            "Cần loại bỏ", "expired", self.theme
        )
        self.low_stock_card = StatCard(
            "Tồn kho thấp", 0, "",
            "Dưới ngưỡng (5 đơn vị)", "low_stock", self.theme
        )

        cards_layout.addWidget(self.total_card)
        cards_layout.addWidget(self.expiring_card)
        cards_layout.addWidget(self.expired_card)
        cards_layout.addWidget(self.low_stock_card)

        layout.addLayout(cards_layout)

        # ── Hàng biểu đồ ──
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(Theme.SPACING_BASE * 2)

        # Biểu đồ tròn - Trạng thái hạn sử dụng
        pie_container = QFrame()
        pie_container.setFrameShape(QFrame.Shape.NoFrame)
        pie_container.setObjectName("chart_card")
        pie_layout = QVBoxLayout(pie_container)
        pie_layout.setContentsMargins(16, 16, 16, 16)

        pie_title = QLabel("Trạng thái thuốc")
        pie_title_font = QFont()
        pie_title_font.setPointSize(14)
        pie_title_font.setBold(True)
        pie_title.setFont(pie_title_font)
        pie_layout.addWidget(pie_title)

        self.pie_chart_canvas = self._create_canvas(figsize=(5, 3.5))
        self.pie_ax = self.pie_chart_canvas.figure.add_subplot(111)
        pie_layout.addWidget(self.pie_chart_canvas)

        charts_layout.addWidget(pie_container, 2)

        # Biểu đồ cột - Top 10
        bar_container = QFrame()
        bar_container.setFrameShape(QFrame.Shape.NoFrame)
        bar_container.setObjectName("chart_card")
        bar_layout = QVBoxLayout(bar_container)
        bar_layout.setContentsMargins(16, 16, 16, 16)

        bar_title = QLabel("Top 10 loại thuốc nhiều nhất")
        bar_title_font = QFont()
        bar_title_font.setPointSize(14)
        bar_title_font.setBold(True)
        bar_title.setFont(bar_title_font)
        bar_layout.addWidget(bar_title)

        self.bar_chart_canvas = self._create_canvas(figsize=(6, 3.5))
        self.bar_ax = self.bar_chart_canvas.figure.add_subplot(111)
        bar_layout.addWidget(self.bar_chart_canvas)

        charts_layout.addWidget(bar_container, 3)

        layout.addLayout(charts_layout)

        # ── Hàng bảng cảnh báo ──
        alerts_layout = QHBoxLayout()
        alerts_layout.setSpacing(Theme.SPACING_BASE * 2)

        # Bảng thuốc sắp hết hạn
        expiry_container = QFrame()
        expiry_container.setFrameShape(QFrame.Shape.NoFrame)
        expiry_container.setObjectName("alert_card")
        expiry_inner = QVBoxLayout(expiry_container)
        expiry_inner.setContentsMargins(16, 16, 16, 16)

        expiry_header = QHBoxLayout()
        expiry_title = QLabel("Thuốc sắp hết hạn")
        expiry_title_font = QFont()
        expiry_title_font.setPointSize(13)
        expiry_title_font.setBold(True)
        expiry_title.setFont(expiry_title_font)
        expiry_header.addWidget(expiry_title)
        expiry_header.addStretch()
        expiry_inner.addLayout(expiry_header)

        self.expiry_table = self._create_alert_table(
            ["Tên thuốc", "HSD", "Vị trí kệ"]
        )
        expiry_inner.addWidget(self.expiry_table)
        alerts_layout.addWidget(expiry_container)

        # Bảng thuốc tồn kho thấp
        stock_container = QFrame()
        stock_container.setFrameShape(QFrame.Shape.NoFrame)
        stock_container.setObjectName("alert_card")
        stock_inner = QVBoxLayout(stock_container)
        stock_inner.setContentsMargins(16, 16, 16, 16)

        stock_header = QHBoxLayout()
        stock_title = QLabel("Tồn kho thấp")
        stock_title_font = QFont()
        stock_title_font.setPointSize(13)
        stock_title_font.setBold(True)
        stock_title.setFont(stock_title_font)
        stock_header.addWidget(stock_title)
        stock_header.addStretch()
        stock_inner.addLayout(stock_header)

        self.stock_table = self._create_alert_table(
            ["Tên thuốc", "Vị trí kệ", "Số lượng"]
        )
        stock_inner.addWidget(self.stock_table)
        alerts_layout.addWidget(stock_container)

        layout.addLayout(alerts_layout)
        layout.addStretch()

        scroll.setWidget(main_widget)

        # Bố cục ngoài cùng
        main_outer = QVBoxLayout()
        main_outer.setContentsMargins(0, 0, 0, 0)
        main_outer.addWidget(scroll)
        self.setLayout(main_outer)

    # ── Phương thức trợ giúp tạo widget ──

    def _create_canvas(self, figsize=(5, 3.5)) -> FigureCanvasQTAgg:
        """Tạo canvas Matplotlib với kích thước chỉ định."""
        fig = Figure(figsize=figsize, dpi=100)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
        return FigureCanvasQTAgg(fig)

    def _create_alert_table(self, headers: list) -> QTableWidget:
        """Tạo bảng cảnh báo với tiêu đề cột cho trước."""
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setMaximumHeight(200)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, len(headers)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        return table

    # ── Tải dữ liệu (gọi DashboardManager rồi render) ──

    def load_data(self, medicines: List[Medicine]):
        """
        Tải dữ liệu thuốc và cập nhật toàn bộ dashboard.

        Ủy quyền xử lý dữ liệu cho DashboardManager,
        sau đó hiển thị kết quả lên giao diện.

        Tham số:
            medicines: Danh sách đối tượng Medicine
        """
        # Lấy dữ liệu đã xử lý từ DashboardManager
        stats = self.manager.get_statistics(medicines)
        pie_data = self.manager.get_pie_chart_data(
            medicines,
            chart_colors=(Theme.CHART_GREEN, Theme.CHART_ORANGE, Theme.CHART_RED)
        )
        bar_data = self.manager.get_bar_chart_data(medicines)
        expiry_items = self.manager.get_expiring_medicines(medicines)
        low_stock_items = self.manager.get_low_stock_medicines(medicines)

        # Render dữ liệu lên giao diện
        self._render_statistics(stats)
        self._render_pie_chart(pie_data)
        self._render_bar_chart(bar_data)
        self._render_expiry_table(expiry_items)
        self._render_stock_table(low_stock_items)

    # ── Render thẻ KPI ──

    def _render_statistics(self, stats: DashboardStats):
        """Cập nhật giá trị các thẻ thống kê."""
        self.total_card.update_value(stats.total)
        self.expired_card.update_value(stats.expired)
        self.expiring_card.update_value(stats.expiring)
        self.low_stock_card.update_value(stats.low_stock)

    # ── Render biểu đồ tròn ──

    def _render_pie_chart(self, data: PieChartData):
        """Vẽ biểu đồ tròn (donut) từ dữ liệu đã xử lý."""
        self.pie_ax.clear()

        bg_color = self.theme.get_color('surface')
        text_color = self.theme.get_color('text_primary')

        if not data.has_data:
            self.pie_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.pie_ax.transAxes
            )
        else:
            wedges, texts, autotexts = self.pie_ax.pie(
                data.sizes,
                labels=data.labels,
                colors=data.colors,
                autopct='%1.0f%%',
                startangle=90,
                pctdistance=0.75,
                wedgeprops=dict(width=0.4, edgecolor=bg_color, linewidth=2),
                textprops={'fontsize': 9, 'color': text_color}
            )

            for t in autotexts:
                t.set_fontsize(8)
                t.set_fontweight('bold')
                t.set_color('#FFFFFF')

        self.pie_ax.set_facecolor(bg_color)
        self.pie_chart_canvas.figure.patch.set_facecolor(bg_color)
        self.pie_chart_canvas.draw()

    # ── Render biểu đồ cột ──

    def _render_bar_chart(self, data: BarChartData):
        """Vẽ biểu đồ cột từ dữ liệu đã xử lý."""
        self.bar_ax.clear()

        bg_color = self.theme.get_color('surface')
        secondary_color = self.theme.get_color('text_secondary')

        if not data.has_data:
            self.bar_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.bar_ax.transAxes
            )
            self.bar_ax.set_facecolor(bg_color)
            self.bar_chart_canvas.figure.patch.set_facecolor(bg_color)
            self.bar_chart_canvas.draw()
            return

        # Vẽ cột
        bars = self.bar_ax.bar(
            range(len(data.names)), data.quantities,
            color=Theme.CHART_BLUE,
            width=0.6,
            edgecolor='none',
            zorder=3
        )

        for bar in bars:
            bar.set_linewidth(0)

        self.bar_ax.set_xticks(range(len(data.names)))
        self.bar_ax.set_xticklabels(
            data.names, rotation=45, ha='right',
            fontsize=8, color=secondary_color
        )
        self.bar_ax.tick_params(axis='y', colors=secondary_color, labelsize=9)

        # Dọn dẹp trục
        self.bar_ax.spines['top'].set_visible(False)
        self.bar_ax.spines['right'].set_visible(False)
        self.bar_ax.spines['left'].set_color(self.theme.get_color('border'))
        self.bar_ax.spines['bottom'].set_color(self.theme.get_color('border'))

        # Thêm lưới
        self.bar_ax.yaxis.grid(True, alpha=0.3, color=self.theme.get_color('border'))
        self.bar_ax.set_axisbelow(True)

        self.bar_ax.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.patch.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.tight_layout()
        self.bar_chart_canvas.draw()

    # ── Render bảng cảnh báo ──

    def _render_expiry_table(self, items: list):
        """Cập nhật bảng thuốc sắp hết hạn."""
        self.expiry_table.setRowCount(0)

        for item in items:
            row = self.expiry_table.rowCount()
            self.expiry_table.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.expiry_table.setItem(row, 0, name_item)

            date_item = QTableWidgetItem(item.expiry_date)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.expiry_table.setItem(row, 1, date_item)

            days_item = QTableWidgetItem(str(item.days_left))
            days_item.setFlags(days_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            days_item.setForeground(QColor(Theme.CHART_ORANGE))
            days_font = days_item.font()
            days_font.setBold(True)
            days_item.setFont(days_font)
            self.expiry_table.setItem(row, 2, days_item)

    def _render_stock_table(self, items: list):
        """Cập nhật bảng thuốc tồn kho thấp."""
        self.stock_table.setRowCount(0)

        for item in items:
            row = self.stock_table.rowCount()
            self.stock_table.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.stock_table.setItem(row, 0, name_item)

            shelf_item = QTableWidgetItem(item.shelf_id)
            shelf_item.setFlags(shelf_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.stock_table.setItem(row, 1, shelf_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setFlags(qty_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            qty_item.setForeground(QColor(Theme.CHART_RED))
            qty_font = qty_item.font()
            qty_font.setBold(True)
            qty_item.setFont(qty_font)
            self.stock_table.setItem(row, 2, qty_item)

    # ── Áp dụng chủ đề ──

    def _apply_theme(self):
        """Áp dụng stylesheet chủ đề."""
        c = self.theme

        # Kiểu cho các container thẻ
        card_style = (
            f"QFrame#chart_card, QFrame#alert_card {{"
            f"  background-color: {c.get_color('surface')};"
            f"  border: 1px solid {c.get_color('border')};"
            f"  border-radius: {Theme.BORDER_RADIUS}px;"
            f"}}"
        )
        self.setStyleSheet(card_style)

        # Cập nhật màu nền biểu đồ
        bg_color = c.get_color('surface')
        text_color = c.get_color('text_primary')

        for canvas in [self.pie_chart_canvas, self.bar_chart_canvas]:
            canvas.figure.patch.set_facecolor(bg_color)
            for ax in canvas.figure.get_axes():
                ax.set_facecolor(bg_color)
                ax.tick_params(colors=text_color)
                ax.xaxis.label.set_color(text_color)
                ax.yaxis.label.set_color(text_color)
                ax.title.set_color(text_color)
                for spine in ax.spines.values():
                    spine.set_edgecolor(c.get_color('border'))
