"""
Dashboard — PHARMA.SYS Statistics and Charts View.

Features:
- 4 colored KPI stat cards (Total, Expiring, Expired, Low Stock)
- Donut chart for expiry distribution
- Vertical bar chart for top medicines by stock
- Approaching Expiry quick list
- Low Stock Items quick list
"""
from typing import List, Optional
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QScrollArea, QFrame, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from src.models import Medicine
from src.alerts import AlertSystem
from src.ui.theme import Theme


class StatCard(QFrame):
    """
    KPI Card widget with colored background.

    Each card displays a number, label, icon, and optional subtitle.
    Background color is determined by card_type.
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
        Initialize stat card.

        Args:
            title: Card title
            value: Statistic value to display
            icon: Emoji icon
            subtitle: Description subtitle
            card_type: 'total', 'expiring', 'expired', 'low_stock'
            theme: Theme instance
            parent: Parent widget
        """
        super().__init__(parent)

        self.theme = theme or Theme()
        self.card_type = card_type
        self.title_text = title
        self.subtitle_text = subtitle

        self.setup_ui(title, value, icon, subtitle)

    def setup_ui(self, title: str, value: int, icon: str, subtitle: str):
        """Setup card UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.CARD_PADDING + 4,
            Theme.CARD_PADDING,
            Theme.CARD_PADDING + 4,
            Theme.CARD_PADDING
        )
        layout.setSpacing(4)

        # Top row: title + icon
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

        # Value
        self.value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(32)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(
            "color: #FFFFFF; background: transparent;"
        )
        layout.addWidget(self.value_label)

        # Subtitle
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 12px; "
            "background: transparent;"
        )
        layout.addWidget(self.subtitle_label)

        self.setLayout(layout)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(120)

        # Apply card color
        self.setStyleSheet(self.theme.get_stat_card_style(self.card_type))

    def update_value(self, value: int, subtitle: str = ""):
        """Update the displayed value and subtitle."""
        self.value_label.setText(str(value))
        if subtitle:
            self.subtitle_label.setText(subtitle)


class Dashboard(QWidget):
    """
    Dashboard widget with KPI cards, charts, and alert lists.

    Features:
    - 4 colored summary statistic cards
    - Donut chart showing expiry distribution
    - Bar chart showing top 10 medicines by stock
    - Quick alert lists (approaching expiry, low stock)
    """

    def __init__(self, parent=None, theme: Optional[Theme] = None):
        """
        Initialize Dashboard.

        Args:
            parent: Parent widget
            theme: Theme instance for styling
        """
        super().__init__(parent)

        self.theme = theme or Theme()
        self.alert_system = AlertSystem()
        self.medicines: List[Medicine] = []

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        """Setup dashboard UI components."""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(Theme.SPACING_BASE * 3)
        layout.setContentsMargins(
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 2,
            Theme.SPACING_BASE * 3,
            Theme.SPACING_BASE * 3
        )

        # ── 4 KPI Cards ──
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

        # ── Charts Row ──
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(Theme.SPACING_BASE * 2)

        # Donut chart - Expiry Status
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

        self.pie_chart_canvas = self.create_pie_chart()
        pie_layout.addWidget(self.pie_chart_canvas)

        charts_layout.addWidget(pie_container, 2)

        # Bar chart - Top 10
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

        self.bar_chart_canvas = self.create_bar_chart()
        bar_layout.addWidget(self.bar_chart_canvas)

        charts_layout.addWidget(bar_container, 3)

        layout.addLayout(charts_layout)

        # ── Alert Quick Lists Row ──
        alerts_layout = QHBoxLayout()
        alerts_layout.setSpacing(Theme.SPACING_BASE * 2)

        # Approaching Expiry table
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

        self.expiry_table = QTableWidget()
        self.expiry_table.setColumnCount(3)
        self.expiry_table.setHorizontalHeaderLabels([
            "Tên thuốc", "HSD", "Vị trí kệ"
        ])
        self.expiry_table.verticalHeader().setVisible(False)
        self.expiry_table.setAlternatingRowColors(True)
        self.expiry_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expiry_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.expiry_table.setMaximumHeight(200)
        header_e = self.expiry_table.horizontalHeader()
        header_e.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_e.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_e.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        expiry_inner.addWidget(self.expiry_table)

        alerts_layout.addWidget(expiry_container)

        # Low Stock table
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

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels([
            "Tên thuốc", "Vị trí kệ", "Số lượng"
        ])
        self.stock_table.verticalHeader().setVisible(False)
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stock_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stock_table.setMaximumHeight(200)
        header_s = self.stock_table.horizontalHeader()
        header_s.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_s.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_s.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        stock_inner.addWidget(self.stock_table)

        alerts_layout.addWidget(stock_container)

        layout.addLayout(alerts_layout)

        layout.addStretch()

        scroll.setWidget(main_widget)

        # Main layout
        main_outer = QVBoxLayout()
        main_outer.setContentsMargins(0, 0, 0, 0)
        main_outer.addWidget(scroll)
        self.setLayout(main_outer)

    def create_pie_chart(self) -> FigureCanvasQTAgg:
        """
        Create donut chart for expiry distribution.

        Returns:
            Matplotlib canvas widget
        """
        fig = Figure(figsize=(5, 3.5), dpi=100)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
        self.pie_ax = fig.add_subplot(111)

        canvas = FigureCanvasQTAgg(fig)
        return canvas

    def create_bar_chart(self) -> FigureCanvasQTAgg:
        """
        Create bar chart for top medicines by quantity.

        Returns:
            Matplotlib canvas widget
        """
        fig = Figure(figsize=(6, 3.5), dpi=100)
        self.bar_ax = fig.add_subplot(111)

        canvas = FigureCanvasQTAgg(fig)
        return canvas

    def load_data(self, medicines: List[Medicine]):
        """
        Load medicine data and update dashboard.

        Args:
            medicines: List of Medicine objects
        """
        self.medicines = medicines
        self.update_statistics()
        self.update_charts()
        self.update_alert_lists()

    def update_statistics(self):
        """Update statistic cards with current data."""
        summary = self.alert_system.get_alert_summary(self.medicines)

        total = summary['total_medicines']
        expired = summary['expired']
        expiring = summary['expiring_soon']
        low_stock_count = summary['low_stock'] + summary['out_of_stock']

        self.total_card.update_value(total)
        self.expired_card.update_value(expired)
        self.expiring_card.update_value(expiring)
        self.low_stock_card.update_value(low_stock_count)

    def update_charts(self):
        """Update all charts with current data."""
        self.update_pie_chart()
        self.update_bar_chart()

    def update_pie_chart(self):
        """Update expiry distribution donut chart."""
        self.pie_ax.clear()

        bg_color = self.theme.get_color('surface')
        text_color = self.theme.get_color('text_primary')

        if not self.medicines:
            self.pie_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.pie_ax.transAxes
            )
            self.pie_ax.set_facecolor(bg_color)
            self.pie_chart_canvas.figure.patch.set_facecolor(bg_color)
            self.pie_chart_canvas.draw()
            return

        # Categorize medicines
        expired = len([m for m in self.medicines if m.is_expired()])
        expiring = len([
            m for m in self.medicines
            if not m.is_expired() and m.days_until_expiry() <= 30
        ])
        normal = len(self.medicines) - expired - expiring

        # Data
        sizes = [normal, expiring, expired]
        labels = ['Bình thường', 'Sắp hết hạn', 'Đã hết hạn']
        colors = [
            Theme.CHART_GREEN,
            Theme.CHART_ORANGE,
            Theme.CHART_RED
        ]

        # Remove zero slices
        sizes_f, labels_f, colors_f = [], [], []
        for i, size in enumerate(sizes):
            if size > 0:
                sizes_f.append(size)
                labels_f.append(f'{labels[i]}\n({size})')
                colors_f.append(colors[i])

        if not sizes_f:
            self.pie_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.pie_ax.transAxes
            )
        else:
            # Donut chart (with center hole)
            wedges, texts, autotexts = self.pie_ax.pie(
                sizes_f,
                labels=labels_f,
                colors=colors_f,
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

    def update_bar_chart(self):
        """Update top medicines by quantity bar chart."""
        self.bar_ax.clear()

        bg_color = self.theme.get_color('surface')
        text_color = self.theme.get_color('text_primary')
        secondary_color = self.theme.get_color('text_secondary')

        if not self.medicines:
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

        # Sort and take top 10
        sorted_meds = sorted(
            self.medicines,
            key=lambda m: m.quantity,
            reverse=True
        )[:10]

        if not sorted_meds:
            self.bar_ax.set_facecolor(bg_color)
            self.bar_chart_canvas.figure.patch.set_facecolor(bg_color)
            self.bar_chart_canvas.draw()
            return

        # Prepare data
        names = [m.name[:15] + '...' if len(m.name) > 15 else m.name
                 for m in sorted_meds]
        quantities = [m.quantity for m in sorted_meds]

        # Vertical bar chart with primary blue
        bars = self.bar_ax.bar(
            range(len(names)), quantities,
            color=Theme.CHART_BLUE,
            width=0.6,
            edgecolor='none',
            zorder=3
        )

        # Rounded bar tops effect
        for bar in bars:
            bar.set_linewidth(0)

        self.bar_ax.set_xticks(range(len(names)))
        self.bar_ax.set_xticklabels(
            names, rotation=45, ha='right',
            fontsize=8, color=secondary_color
        )
        self.bar_ax.tick_params(axis='y', colors=secondary_color, labelsize=9)

        # Clean up axes
        self.bar_ax.spines['top'].set_visible(False)
        self.bar_ax.spines['right'].set_visible(False)
        self.bar_ax.spines['left'].set_color(self.theme.get_color('border'))
        self.bar_ax.spines['bottom'].set_color(self.theme.get_color('border'))

        # Add grid
        self.bar_ax.yaxis.grid(True, alpha=0.3, color=self.theme.get_color('border'))
        self.bar_ax.set_axisbelow(True)

        self.bar_ax.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.patch.set_facecolor(bg_color)
        self.bar_chart_canvas.figure.tight_layout()
        self.bar_chart_canvas.draw()

    def update_alert_lists(self):
        """Update the approaching expiry and low stock quick lists."""
        self._update_expiry_list()
        self._update_stock_list()

    def _update_expiry_list(self):
        """Update approaching expiry table."""
        self.expiry_table.setRowCount(0)

        # Get medicines expiring soon (not already expired), sorted by days left
        expiring = [
            m for m in self.medicines
            if not m.is_expired() and m.days_until_expiry() <= 30
        ]
        expiring.sort(key=lambda m: m.days_until_expiry())

        for m in expiring[:5]:  # Show top 5
            row = self.expiry_table.rowCount()
            self.expiry_table.insertRow(row)

            name_item = QTableWidgetItem(m.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.expiry_table.setItem(row, 0, name_item)

            date_item = QTableWidgetItem(m.expiry_date.strftime("%Y-%m-%d"))
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.expiry_table.setItem(row, 1, date_item)

            days_left = m.days_until_expiry()
            days_item = QTableWidgetItem(f"{days_left}")
            days_item.setFlags(days_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            days_item.setForeground(QColor(Theme.CHART_ORANGE))
            days_font = days_item.font()
            days_font.setBold(True)
            days_item.setFont(days_font)
            self.expiry_table.setItem(row, 2, days_item)

    def _update_stock_list(self):
        """Update low stock items table."""
        self.stock_table.setRowCount(0)

        # Get low stock medicines (quantity <= 5), sorted by quantity
        low_stock = [
            m for m in self.medicines
            if m.quantity <= 5
        ]
        low_stock.sort(key=lambda m: m.quantity)

        for m in low_stock[:5]:  # Show top 5
            row = self.stock_table.rowCount()
            self.stock_table.insertRow(row)

            name_item = QTableWidgetItem(m.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.stock_table.setItem(row, 0, name_item)

            shelf_item = QTableWidgetItem(m.shelf_id)
            shelf_item.setFlags(shelf_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.stock_table.setItem(row, 1, shelf_item)

            qty_item = QTableWidgetItem(str(m.quantity))
            qty_item.setFlags(qty_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            qty_item.setForeground(QColor(Theme.CHART_RED))
            qty_font = qty_item.font()
            qty_font.setBold(True)
            qty_item.setFont(qty_font)
            self.stock_table.setItem(row, 2, qty_item)

    def apply_theme(self):
        """Apply theme stylesheet."""
        c = self.theme

        # Card containers styling
        card_style = (
            f"QFrame#chart_card, QFrame#alert_card {{"
            f"  background-color: {c.get_color('surface')};"
            f"  border: 1px solid {c.get_color('border')};"
            f"  border-radius: {Theme.BORDER_RADIUS}px;"
            f"}}"
        )
        self.setStyleSheet(card_style)

        # Update chart background colors
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
