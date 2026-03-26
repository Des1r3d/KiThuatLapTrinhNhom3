"""
Dashboard — Giao diện Thống kê và Biểu đồ PHARMA.SYS.

Uses Qt Designer-generated UI from dashboard_ui.py for layout.
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
    QWidget, QVBoxLayout, QHeaderView,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.models import Medicine
from src.dashboard_manager import (
    DashboardManager, DashboardStats,
    PieChartData, BarChartData,
)
from src.ui.theme import Theme
from src.ui.generated.dashboard_ui import Ui_DashboardWidget


class Dashboard(QWidget):
    """
    Widget Dashboard với thẻ KPI, biểu đồ và bảng cảnh báo.

    Uses Ui_DashboardWidget from dashboard_ui.py for layout.
    CHỈ chứa mã giao diện. Mọi logic xử lý dữ liệu được
    ủy quyền cho DashboardManager (src/dashboard_manager.py).
    """

    def __init__(self, parent=None, theme: Optional[Theme] = None):
        super().__init__(parent)

        self.theme = theme or Theme()
        self.manager = DashboardManager()

        self._setup_ui()
        self._apply_theme()

    def _setup_ui(self):
        """Thiết lập UI từ generated class và thay thế chart placeholders."""
        self.ui = Ui_DashboardWidget()
        self.ui.setupUi(self)

        # ── Thay thế chart placeholders bằng matplotlib canvases ──
        self.pie_chart_canvas = self._create_canvas(figsize=(5, 3.5))
        self.pie_ax = self.pie_chart_canvas.figure.add_subplot(111)
        self._replace_placeholder(
            self.ui.pie_layout,
            self.ui.widget_pie_placeholder,
            self.pie_chart_canvas
        )

        self.bar_chart_canvas = self._create_canvas(figsize=(6, 3.5))
        self.bar_ax = self.bar_chart_canvas.figure.add_subplot(111)
        self._replace_placeholder(
            self.ui.bar_layout,
            self.ui.widget_bar_placeholder,
            self.bar_chart_canvas
        )

        # ── Cấu hình table headers ──
        self._configure_table(self.ui.tbl_expiry)
        self._configure_table(self.ui.tbl_stock)

        # ── Áp dụng stylesheet cho card frames ──
        self.ui.card_total.setStyleSheet(
            self.theme.get_stat_card_style("total")
        )
        self.ui.card_expiring.setStyleSheet(
            self.theme.get_stat_card_style("expiring")
        )
        self.ui.card_expired.setStyleSheet(
            self.theme.get_stat_card_style("expired")
        )
        self.ui.card_low_stock.setStyleSheet(
            self.theme.get_stat_card_style("low_stock")
        )

        # ── Đặt objectName cho chart/alert frames (dùng cho theme stylesheet) ──
        self.ui.frame_pie_chart.setObjectName("chart_card")
        self.ui.frame_bar_chart.setObjectName("chart_card")
        self.ui.frame_expiry_alerts.setObjectName("alert_card")
        self.ui.frame_stock_alerts.setObjectName("alert_card")

    @staticmethod
    def _replace_placeholder(layout: QVBoxLayout, placeholder: QWidget, replacement: QWidget):
        """Thay thế placeholder widget bằng widget thực trong layout."""
        index = layout.indexOf(placeholder)
        layout.removeWidget(placeholder)
        placeholder.deleteLater()
        layout.insertWidget(index, replacement)

    @staticmethod
    def _create_canvas(figsize=(5, 3.5)) -> FigureCanvasQTAgg:
        """Tạo canvas Matplotlib với kích thước chỉ định."""
        fig = Figure(figsize=figsize, dpi=100)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
        return FigureCanvasQTAgg(fig)

    @staticmethod
    def _configure_table(table):
        """Cấu hình header cho bảng cảnh báo."""
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

    # ── Tải dữ liệu ──

    def load_data(self, medicines: List[Medicine]):
        """
        Tải dữ liệu thuốc và cập nhật toàn bộ dashboard.

        Ủy quyền xử lý cho DashboardManager, sau đó hiển thị lên giao diện.
        """
        stats = self.manager.get_statistics(medicines)
        pie_data = self.manager.get_pie_chart_data(
            medicines,
            chart_colors=(Theme.CHART_GREEN, Theme.CHART_ORANGE, Theme.CHART_RED)
        )
        bar_data = self.manager.get_bar_chart_data(medicines)
        expiry_items = self.manager.get_expiring_medicines(medicines)
        low_stock_items = self.manager.get_low_stock_medicines(medicines)

        self._render_statistics(stats)
        self._render_pie_chart(pie_data)
        self._render_bar_chart(bar_data)
        self._render_expiry_table(expiry_items)
        self._render_stock_table(low_stock_items)

    # ── Render thẻ KPI ──

    def _render_statistics(self, stats: DashboardStats):
        """Cập nhật giá trị các thẻ thống kê."""
        self.ui.lbl_total_value.setText(str(stats.total))
        self.ui.lbl_expiring_value.setText(str(stats.expiring))
        self.ui.lbl_expired_value.setText(str(stats.expired))
        self.ui.lbl_low_stock_value.setText(str(stats.low_stock))

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

        self.bar_ax.spines['top'].set_visible(False)
        self.bar_ax.spines['right'].set_visible(False)
        self.bar_ax.spines['left'].set_color(self.theme.get_color('border'))
        self.bar_ax.spines['bottom'].set_color(self.theme.get_color('border'))

        self.bar_ax.yaxis.grid(True, alpha=0.3, color=self.theme.get_color('border'))
        self.bar_ax.set_axisbelow(True)

        self.bar_ax.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.patch.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.tight_layout()
        self.bar_chart_canvas.draw()

    # ── Render bảng cảnh báo ──

    def _render_expiry_table(self, items: list):
        """Cập nhật bảng thuốc sắp hết hạn."""
        self.ui.tbl_expiry.setRowCount(0)

        for item in items:
            row = self.ui.tbl_expiry.rowCount()
            self.ui.tbl_expiry.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_expiry.setItem(row, 0, name_item)

            date_item = QTableWidgetItem(item.expiry_date)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_expiry.setItem(row, 1, date_item)

            days_item = QTableWidgetItem(str(item.days_left))
            days_item.setFlags(days_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            days_item.setForeground(QColor(Theme.CHART_ORANGE))
            days_font = days_item.font()
            days_font.setBold(True)
            days_item.setFont(days_font)
            self.ui.tbl_expiry.setItem(row, 2, days_item)

    def _render_stock_table(self, items: list):
        """Cập nhật bảng thuốc tồn kho thấp."""
        self.ui.tbl_stock.setRowCount(0)

        for item in items:
            row = self.ui.tbl_stock.rowCount()
            self.ui.tbl_stock.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_stock.setItem(row, 0, name_item)

            shelf_item = QTableWidgetItem(item.shelf_id)
            shelf_item.setFlags(shelf_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tbl_stock.setItem(row, 1, shelf_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setFlags(qty_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            qty_item.setForeground(QColor(Theme.CHART_RED))
            qty_font = qty_item.font()
            qty_font.setBold(True)
            qty_item.setFont(qty_font)
            self.ui.tbl_stock.setItem(row, 2, qty_item)

    # ── Áp dụng chủ đề ──

    def _apply_theme(self):
        """Áp dụng stylesheet chủ đề."""
        c = self.theme

        card_style = (
            f"QFrame#chart_card, QFrame#alert_card {{"
            f"  background-color: {c.get_color('surface')};"
            f"  border: 1px solid {c.get_color('border')};"
            f"  border-radius: {Theme.BORDER_RADIUS}px;"
            f"}}"
        )
        self.setStyleSheet(card_style)

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
