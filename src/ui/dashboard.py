"""
Dashboard - Statistics and charts view.

Features:
- Alert summary cards
- Pie chart for expiry distribution
- Bar chart for top medicines by quantity
- Real-time statistics
"""
from typing import List, Optional
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from src.models import Medicine
from src.alerts import AlertSystem
from src.ui.theme import Theme


class StatCard(QFrame):
    """
    Card widget for displaying a statistic.
    
    Shows a number with a label and optional color coding.
    """
    
    def __init__(
        self, 
        title: str, 
        value: int, 
        color_type: str = "normal",
        theme: Optional[Theme] = None,
        parent=None
    ):
        """
        Initialize stat card.
        
        Args:
            title: Card title
            value: Statistic value to display
            color_type: Color type ('danger', 'warning', 'low_stock', 'success')
            theme: Theme instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.theme = theme or Theme()
        self.color_type = color_type
        
        self.setup_ui(title, value)
    
    def setup_ui(self, title: str, value: int):
        """Setup card UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.CARD_PADDING,
            Theme.CARD_PADDING,
            Theme.CARD_PADDING,
            Theme.CARD_PADDING
        )
        
        # Value
        value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(32)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Apply color
        if self.color_type != "normal":
            colors = self.theme.get_alert_colors(self.color_type)
            value_label.setStyleSheet(f"color: {colors['text']};")
        
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setProperty("secondary", True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        self.setLayout(layout)
        self.setFrameShape(QFrame.Shape.StyledPanel)


class Dashboard(QWidget):
    """
    Dashboard widget with statistics and charts.
    
    Features:
    - Summary statistics cards
    - Pie chart showing expiry distribution
    - Bar chart showing top 10 medicines by quantity
    - Automatic refresh on data update
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
        
        # Title
        title_label = QLabel("Bảng Điều Khiển")
        title_font = QFont()
        title_font.setPointSize(Theme.FONT_SIZE_H1)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Statistics Cards
        stats_group = QGroupBox("Tổng quan")
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(Theme.SPACING_BASE * 2)
        
        self.total_card = StatCard("Tổng số thuốc", 0, "normal", self.theme)
        self.expired_card = StatCard("Đã hết hạn", 0, "danger", self.theme)
        self.expiring_card = StatCard("Sắp hết hạn", 0, "warning", self.theme)
        self.low_stock_card = StatCard("Tồn kho thấp", 0, "low_stock", self.theme)
        
        stats_layout.addWidget(self.total_card)
        stats_layout.addWidget(self.expired_card)
        stats_layout.addWidget(self.expiring_card)
        stats_layout.addWidget(self.low_stock_card)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Charts section
        charts_group = QGroupBox("Biểu đồ")
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(Theme.SPACING_BASE * 2)
        
        # Pie chart - Expiry distribution
        self.pie_chart_canvas = self.create_pie_chart()
        charts_layout.addWidget(self.pie_chart_canvas)
        
        # Bar chart - Top medicines
        self.bar_chart_canvas = self.create_bar_chart()
        charts_layout.addWidget(self.bar_chart_canvas)
        
        charts_group.setLayout(charts_layout)
        layout.addWidget(charts_group)
        
        layout.addStretch()
        
        scroll.setWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def create_pie_chart(self) -> FigureCanvasQTAgg:
        """
        Create pie chart for expiry distribution.
        
        Returns:
            Matplotlib canvas widget
        """
        fig = Figure(figsize=(6, 4), dpi=100)
        self.pie_ax = fig.add_subplot(111)
        
        canvas = FigureCanvasQTAgg(fig)
        return canvas
    
    def create_bar_chart(self) -> FigureCanvasQTAgg:
        """
        Create bar chart for top medicines by quantity.
        
        Returns:
            Matplotlib canvas widget
        """
        fig = Figure(figsize=(6, 4), dpi=100)
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
    
    def update_statistics(self):
        """Update statistic cards with current data."""
        summary = self.alert_system.get_alert_summary(self.medicines)
        
        # Update cards
        self.total_card.findChild(QLabel).setText(
            str(summary['total_medicines'])
        )
        self.expired_card.findChild(QLabel).setText(
            str(summary['expired'])
        )
        self.expiring_card.findChild(QLabel).setText(
            str(summary['expiring_soon'])
        )
        # Combine out of stock and low stock
        low_stock_count = summary['low_stock'] + summary['out_of_stock']
        self.low_stock_card.findChild(QLabel).setText(
            str(low_stock_count)
        )
    
    def update_charts(self):
        """Update all charts with current data."""
        self.update_pie_chart()
        self.update_bar_chart()
    
    def update_pie_chart(self):
        """Update expiry distribution pie chart."""
        self.pie_ax.clear()
        
        if not self.medicines:
            self.pie_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray'
            )
            self.pie_chart_canvas.draw()
            return
        
        # Categorize medicines
        expired = len([m for m in self.medicines if m.is_expired()])
        expiring = len([
            m for m in self.medicines 
            if not m.is_expired() and m.days_until_expiry() <= 30
        ])
        normal = len(self.medicines) - expired - expiring
        
        # Get theme colors
        colors_map = {
            'danger': self.theme.get_alert_colors('danger')['text'],
            'warning': self.theme.get_alert_colors('warning')['text'],
            'success': self.theme.get_alert_colors('success')['text']
        }
        
        # Data for pie chart
        sizes = [expired, expiring, normal]
        labels = [f'Hết hạn\n({expired})', f'Sắp hết hạn\n({expiring})', f'Bình thường\n({normal})']
        colors = [colors_map['danger'], colors_map['warning'], colors_map['success']]
        
        # Remove zero slices
        sizes_filtered = []
        labels_filtered = []
        colors_filtered = []
        for i, size in enumerate(sizes):
            if size > 0:
                sizes_filtered.append(size)
                labels_filtered.append(labels[i])
                colors_filtered.append(colors[i])
        
        if not sizes_filtered:
            self.pie_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray'
            )
        else:
            self.pie_ax.pie(
                sizes_filtered,
                labels=labels_filtered,
                colors=colors_filtered,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10}
            )
            self.pie_ax.set_title('Phân bố hạn sử dụng', fontsize=12, fontweight='bold')
        
        self.pie_chart_canvas.draw()
    
    def update_bar_chart(self):
        """Update top medicines by quantity bar chart."""
        self.bar_ax.clear()
        
        if not self.medicines:
            self.bar_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.bar_ax.transAxes
            )
            self.bar_chart_canvas.draw()
            return
        
        # Sort by quantity and take top 10
        sorted_meds = sorted(
            self.medicines,
            key=lambda m: m.quantity,
            reverse=True
        )[:10]
        
        if not sorted_meds:
            self.bar_ax.text(
                0.5, 0.5, 'Không có dữ liệu',
                ha='center', va='center',
                fontsize=14, color='gray',
                transform=self.bar_ax.transAxes
            )
            self.bar_chart_canvas.draw()
            return
        
        # Prepare data
        names = [m.name[:20] + '...' if len(m.name) > 20 else m.name 
                 for m in sorted_meds]
        quantities = [m.quantity for m in sorted_meds]
        
        # Color bars based on stock level
        colors = []
        for m in sorted_meds:
            if m.quantity == 0:
                colors.append(self.theme.get_alert_colors('danger')['text'])
            elif m.quantity <= 5:
                colors.append(self.theme.get_alert_colors('low_stock')['text'])
            else:
                colors.append(self.theme.get_color('primary'))
        
        # Create bar chart
        bars = self.bar_ax.barh(names, quantities, color=colors)
        
        self.bar_ax.set_xlabel('Số lượng (đơn vị)', fontsize=10)
        self.bar_ax.set_title('Top 10 thuốc theo tồn kho', fontsize=12, fontweight='bold')
        self.bar_ax.invert_yaxis()  # Highest at top
        
        # Add value labels
        for i, (bar, qty) in enumerate(zip(bars, quantities)):
            self.bar_ax.text(
                qty, i, f' {qty}',
                va='center', fontsize=9
            )
        
        # Adjust layout
        self.bar_chart_canvas.figure.tight_layout()
        self.bar_chart_canvas.draw()
    
    def apply_theme(self):
        """Apply theme stylesheet."""
        self.setStyleSheet(self.theme.get_stylesheet())
        
        # Update chart background colors based on theme
        bg_color = self.theme.get_color('surface')
        text_color = self.theme.get_color('text_primary')
        
        for canvas in [self.pie_chart_canvas, self.bar_chart_canvas]:
            canvas.figure.patch.set_facecolor(bg_color)
            for ax in canvas.figure.get_axes():
                ax.set_facecolor(bg_color)
                ax.tick_params(colors=text_color)
                ax.xaxis.label.set_color(text_color)
                ax.yaxis.label.set_color(text_color)
                ax.title.set_color(text_color)
                for spine in ax.spines.values():
                    spine.set_edgecolor(self.theme.get_color('border'))
