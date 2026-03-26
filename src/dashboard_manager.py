"""
Trình quản lý Dashboard cho Hệ Thống Quản Lý Kho Thuốc.

Module này chứa logic xử lý dữ liệu cho trang Dashboard:
- Tính toán thống kê tổng quan (KPI)
- Chuẩn bị dữ liệu biểu đồ tròn (phân bố hạn sử dụng)
- Chuẩn bị dữ liệu biểu đồ cột (top thuốc theo số lượng)
- Lọc danh sách thuốc sắp hết hạn
- Lọc danh sách thuốc tồn kho thấp
"""
from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import date

from src.models import Medicine
from src.alerts import AlertSystem


@dataclass
class DashboardStats:
    """
    Dữ liệu thống kê tổng quan cho Dashboard.

    Thuộc tính:
        total: Tổng số thuốc
        expired: Số thuốc đã hết hạn
        expiring: Số thuốc sắp hết hạn (trong 30 ngày)
        low_stock: Số thuốc tồn kho thấp (bao gồm hết hàng)
    """
    total: int = 0
    expired: int = 0
    expiring: int = 0
    low_stock: int = 0


@dataclass
class PieChartData:
    """
    Dữ liệu đã xử lý cho biểu đồ tròn (donut).

    Thuộc tính:
        sizes: Danh sách số lượng mỗi phần
        labels: Danh sách nhãn tương ứng
        colors: Danh sách mã màu tương ứng
        has_data: True nếu có dữ liệu để hiển thị
    """
    sizes: List[int] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    colors: List[str] = field(default_factory=list)
    has_data: bool = False


@dataclass
class BarChartData:
    """
    Dữ liệu đã xử lý cho biểu đồ cột.

    Thuộc tính:
        names: Danh sách tên thuốc (đã cắt ngắn nếu cần)
        quantities: Danh sách số lượng tương ứng
        has_data: True nếu có dữ liệu để hiển thị
    """
    names: List[str] = field(default_factory=list)
    quantities: List[int] = field(default_factory=list)
    has_data: bool = False


@dataclass
class ExpiryItem:
    """
    Một mục thuốc sắp hết hạn cho bảng cảnh báo.

    Thuộc tính:
        name: Tên thuốc
        expiry_date: Ngày hết hạn (định dạng chuỗi)
        days_left: Số ngày còn lại
    """
    name: str
    expiry_date: str
    days_left: int


@dataclass
class LowStockItem:
    """
    Một mục thuốc tồn kho thấp cho bảng cảnh báo.

    Thuộc tính:
        name: Tên thuốc
        shelf_id: Vị trí kệ
        quantity: Số lượng hiện tại
    """
    name: str
    shelf_id: str
    quantity: int


class DashboardManager:
    """
    Bộ xử lý dữ liệu trung tâm cho trang Dashboard.

    Nhận danh sách thuốc thô và chuyển đổi thành dữ liệu đã xử lý
    sẵn sàng cho UI hiển thị. Tách biệt logic nghiệp vụ khỏi tầng view.

    Thuộc tính:
        alert_system: Hệ thống cảnh báo để tính thống kê
        expiry_threshold: Ngưỡng ngày sắp hết hạn (mặc định: 30)
        low_stock_threshold: Ngưỡng tồn kho thấp (mặc định: 5)
        max_bar_items: Số lượng thuốc tối đa trong biểu đồ cột (mặc định: 10)
        max_alert_items: Số lượng mục tối đa trong bảng cảnh báo (mặc định: 5)
        max_name_length: Độ dài tối đa tên thuốc trên biểu đồ (mặc định: 15)
    """

    def __init__(
        self,
        expiry_threshold: int = 30,
        low_stock_threshold: int = 5,
        max_bar_items: int = 10,
        max_alert_items: int = 5,
        max_name_length: int = 15
    ):
        """
        Khởi tạo DashboardManager.

        Tham số:
            expiry_threshold: Ngưỡng ngày sắp hết hạn
            low_stock_threshold: Ngưỡng tồn kho thấp
            max_bar_items: Số lượng thuốc tối đa trong biểu đồ cột
            max_alert_items: Số lượng mục tối đa trong bảng cảnh báo
            max_name_length: Độ dài tối đa tên thuốc trên biểu đồ
        """
        self.alert_system = AlertSystem(
            expiry_threshold=expiry_threshold,
            low_stock_threshold=low_stock_threshold
        )
        self.expiry_threshold = expiry_threshold
        self.low_stock_threshold = low_stock_threshold
        self.max_bar_items = max_bar_items
        self.max_alert_items = max_alert_items
        self.max_name_length = max_name_length

    def get_statistics(self, medicines: List[Medicine]) -> DashboardStats:
        """
        Tính toán thống kê tổng quan từ danh sách thuốc.

        Tham số:
            medicines: Danh sách thuốc trong kho

        Trả về:
            DashboardStats chứa các chỉ số KPI
        """
        summary = self.alert_system.get_alert_summary(medicines)
        return DashboardStats(
            total=summary['total_medicines'],
            expired=summary['expired'],
            expiring=summary['expiring_soon'],
            low_stock=summary['low_stock'] + summary['out_of_stock']
        )

    def get_pie_chart_data(
        self,
        medicines: List[Medicine],
        chart_colors: Tuple[str, str, str] = ('#10B981', '#FF8800', '#EF4444')
    ) -> PieChartData:
        """
        Chuẩn bị dữ liệu cho biểu đồ tròn phân bố hạn sử dụng.

        Phân loại thuốc thành 3 nhóm:
        - Bình thường (còn hạn > 30 ngày)
        - Sắp hết hạn (0 < ngày còn lại <= 30)
        - Đã hết hạn

        Tham số:
            medicines: Danh sách thuốc
            chart_colors: Tuple 3 màu (bình_thường, sắp_hết_hạn, đã_hết_hạn)

        Trả về:
            PieChartData đã lọc bỏ các phần có giá trị 0
        """
        if not medicines:
            return PieChartData(has_data=False)

        expired = len([m for m in medicines if m.is_expired()])
        expiring = len([
            m for m in medicines
            if not m.is_expired() and m.days_until_expiry() <= self.expiry_threshold
        ])
        normal = len(medicines) - expired - expiring

        all_sizes = [normal, expiring, expired]
        all_labels = ['Bình thường', 'Sắp hết hạn', 'Đã hết hạn']
        all_colors = list(chart_colors)

        # Lọc bỏ phần có giá trị 0
        sizes, labels, colors = [], [], []
        for i, size in enumerate(all_sizes):
            if size > 0:
                sizes.append(size)
                labels.append(f'{all_labels[i]}\n({size})')
                colors.append(all_colors[i])

        return PieChartData(
            sizes=sizes,
            labels=labels,
            colors=colors,
            has_data=len(sizes) > 0
        )

    def get_bar_chart_data(self, medicines: List[Medicine]) -> BarChartData:
        """
        Chuẩn bị dữ liệu cho biểu đồ cột top thuốc theo số lượng.

        Sắp xếp thuốc theo số lượng giảm dần và lấy top N.
        Tên thuốc được cắt ngắn nếu vượt quá max_name_length.

        Tham số:
            medicines: Danh sách thuốc

        Trả về:
            BarChartData với tên và số lượng đã xử lý
        """
        if not medicines:
            return BarChartData(has_data=False)

        sorted_meds = sorted(
            medicines,
            key=lambda m: m.quantity,
            reverse=True
        )[:self.max_bar_items]

        if not sorted_meds:
            return BarChartData(has_data=False)

        names = [
            m.name[:self.max_name_length] + '...'
            if len(m.name) > self.max_name_length
            else m.name
            for m in sorted_meds
        ]
        quantities = [m.quantity for m in sorted_meds]

        return BarChartData(
            names=names,
            quantities=quantities,
            has_data=True
        )

    def get_expiring_medicines(self, medicines: List[Medicine]) -> List[ExpiryItem]:
        """
        Lấy danh sách thuốc sắp hết hạn cho bảng cảnh báo.

        Lọc thuốc chưa hết hạn nhưng sắp hết hạn (trong ngưỡng),
        sắp xếp theo số ngày còn lại (ít nhất trước).

        Tham số:
            medicines: Danh sách thuốc

        Trả về:
            Danh sách ExpiryItem (tối đa max_alert_items mục)
        """
        expiring = [
            m for m in medicines
            if not m.is_expired() and m.days_until_expiry() <= self.expiry_threshold
        ]
        expiring.sort(key=lambda m: m.days_until_expiry())

        return [
            ExpiryItem(
                name=m.name,
                expiry_date=m.expiry_date.strftime("%Y-%m-%d"),
                days_left=m.days_until_expiry()
            )
            for m in expiring[:self.max_alert_items]
        ]

    def get_low_stock_medicines(self, medicines: List[Medicine]) -> List[LowStockItem]:
        """
        Lấy danh sách thuốc tồn kho thấp cho bảng cảnh báo.

        Lọc thuốc có số lượng <= ngưỡng, sắp xếp theo số lượng tăng dần.

        Tham số:
            medicines: Danh sách thuốc

        Trả về:
            Danh sách LowStockItem (tối đa max_alert_items mục)
        """
        low_stock = [
            m for m in medicines
            if m.quantity <= self.low_stock_threshold
        ]
        low_stock.sort(key=lambda m: m.quantity)

        return [
            LowStockItem(
                name=m.name,
                shelf_id=m.shelf_id,
                quantity=m.quantity
            )
            for m in low_stock[:self.max_alert_items]
        ]
