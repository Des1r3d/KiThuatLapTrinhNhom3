"""
Hệ thống Cảnh báo cho Hệ Thống Quản Lý Kho Thuốc.

Module này cung cấp giám sát cho:
- Thuốc sắp hết hạn (trong ngưỡng có thể cấu hình)
- Thuốc tồn kho thấp (dưới ngưỡng có thể cấu hình)
"""
from datetime import date
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

from src.models import Medicine


class AlertType(Enum):
    """Các loại cảnh báo trong hệ thống."""
    EXPIRED = "expired"
    EXPIRING_SOON = "expiring_soon"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"


@dataclass
class Alert:
    """
    Đại diện một cảnh báo cho thuốc.
    
    Thuộc tính:
        medicine: Thuốc liên quan đến cảnh báo
        alert_type: Loại cảnh báo
        message: Thông báo cảnh báo dễ đọc
        severity: Mức độ nghiêm trọng (1=thấp, 3=cao)
    """
    medicine: Medicine
    alert_type: AlertType
    message: str
    severity: int  # 1 = thấp, 2 = trung bình, 3 = cao

    '''
    Kiểm tra:
        - Thuốc hết hạn (mức độ: 3)
        - Sắp hết hạn (mức độ: 2)
        - Hết hàng (mức độ: 3)
        - Tồn kho thấp (mức độ: 1)
    '''
class AlertSystem:
    """
    Hệ thống giám sát kho và tạo cảnh báo.
    
    Giám sát:
    - Thuốc đã hết hạn
    - Thuốc sắp hết hạn trong ngưỡng
    - Tồn kho thấp
    - Hết hàng
    
    Thuộc tính:
        expiry_threshold: Số ngày trước hạn để kích hoạt cảnh báo (mặc định: 30)
        low_stock_threshold: Ngưỡng số lượng cho tồn kho thấp (mặc định: 5)
    """
    
    def __init__(
        self,
        expiry_threshold: int = 30,
        low_stock_threshold: int = 5
    ):
        """
        Khởi tạo AlertSystem với các ngưỡng.
        
        Tham số:
            expiry_threshold: Số ngày trước hạn để kích hoạt cảnh báo
            low_stock_threshold: Số lượng dưới ngưỡng để kích hoạt cảnh báo
        """
        self.expiry_threshold = expiry_threshold
        self.low_stock_threshold = low_stock_threshold
    
    def check_expiry(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Tìm thuốc đã hết hạn hoặc sắp hết hạn.
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Danh sách thuốc có days_until_expiry <= ngưỡng,
            sắp xếp theo ngày hết hạn (sớm nhất trước)
        """
        expiring = [
            med for med in medicines
            if med.days_until_expiry() <= self.expiry_threshold
        ]
        
        # Sắp xếp theo ngày hết hạn (sớm nhất trước)
        expiring.sort(key=lambda m: m.expiry_date)
        
        return expiring
    
    def check_low_stock(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Tìm thuốc có mức tồn kho thấp.
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Danh sách thuốc có quantity <= ngưỡng,
            sắp xếp theo số lượng (thấp nhất trước)
        """
        low_stock = [
            med for med in medicines
            if med.quantity <= self.low_stock_threshold
        ]
        
        # Sắp xếp theo số lượng (thấp nhất trước)
        low_stock.sort(key=lambda m: m.quantity)
        
        return low_stock
    
    def check_expired(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Tìm thuốc đã hết hạn.
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Danh sách thuốc hết hạn (expiry_date < hôm nay),
            sắp xếp theo ngày hết hạn (cũ nhất trước)
        """
        expired = [med for med in medicines if med.is_expired()]
        
        # Sắp xếp theo ngày hết hạn (cũ nhất trước - quá hạn nhất)
        expired.sort(key=lambda m: m.expiry_date)
        
        return expired
    
    def check_out_of_stock(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Tìm thuốc hoàn toàn hết hàng.
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Danh sách thuốc có quantity == 0, sắp xếp theo tên
        """
        out_of_stock = [med for med in medicines if med.quantity == 0]
        
        # Sắp xếp theo tên để dễ tra cứu
        out_of_stock.sort(key=lambda m: m.name)
        
        return out_of_stock
    
    def generate_alerts(self, medicines: List[Medicine]) -> List[Alert]:
        """
        Tạo tất cả cảnh báo cho danh sách thuốc.
        
        Kiểm tra:
        - Thuốc hết hạn (mức độ: 3)
        - Sắp hết hạn (mức độ: 2)
        - Hết hàng (mức độ: 3)
        - Tồn kho thấp (mức độ: 1)
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Danh sách đối tượng Alert, sắp xếp theo mức độ (cao nhất trước)
        """
        alerts: List[Alert] = []
        
        # Kiểm tra thuốc hết hạn (ưu tiên cao nhất)
        for med in self.check_expired(medicines):
            days_overdue = abs(med.days_until_expiry())
            alerts.append(Alert(
                medicine=med,
                alert_type=AlertType.EXPIRED,
                message=f"'{med.name}' đã hết hạn được {days_overdue} ngày",
                severity=3
            ))
        
        # Kiểm tra sắp hết hạn (loại trừ đã hết hạn)
        for med in self.check_expiry(medicines):
            if not med.is_expired():
                days_left = med.days_until_expiry()
                alerts.append(Alert(
                    medicine=med,
                    alert_type=AlertType.EXPIRING_SOON,
                    message=f"'{med.name}' sẽ hết hạn trong {days_left} ngày",
                    severity=2
                ))
        
        # Kiểm tra hết hàng (ưu tiên cao nhất)
        for med in self.check_out_of_stock(medicines):
            alerts.append(Alert(
                medicine=med,
                alert_type=AlertType.OUT_OF_STOCK,
                message=f"'{med.name}' đã hết hàng",
                severity=3
            ))
        
        # Kiểm tra tồn kho thấp (loại trừ hết hàng - đã xử lý)
        for med in self.check_low_stock(medicines):
            if med.quantity > 0:
                alerts.append(Alert(
                    medicine=med,
                    alert_type=AlertType.LOW_STOCK,
                    message=f"'{med.name}' còn ít hàng, với ({med.quantity} đơn vị còn lại)",
                    severity=1
                ))
        
        # Sắp xếp theo mức độ (cao nhất trước)
        alerts.sort(key=lambda a: a.severity, reverse=True)
        
        return alerts
    
    def get_alert_summary(self, medicines: List[Medicine]) -> dict:
        """
        Lấy thống kê tóm tắt cho cảnh báo.
        
        Tham số:
            medicines: Danh sách thuốc cần kiểm tra
            
        Trả về:
            Dictionary với số lượng cho mỗi loại cảnh báo
        """
        return {
            "expired": len(self.check_expired(medicines)),
            "expiring_soon": len([
                m for m in self.check_expiry(medicines)
                if not m.is_expired()
            ]),
            "out_of_stock": len(self.check_out_of_stock(medicines)),
            "low_stock": len([
                m for m in self.check_low_stock(medicines)
                if m.quantity > 0
            ]),
            "total_medicines": len(medicines)
        }
