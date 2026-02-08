"""
Alert System for Pharmacy Management System.

This module provides monitoring for:
- Expiring medicines (within configurable threshold)
- Low stock medicines (below configurable threshold)
"""
from datetime import date
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

from src.models import Medicine


class AlertType(Enum):
    """Types of alerts in the system."""
    EXPIRED = "expired"
    EXPIRING_SOON = "expiring_soon"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"


@dataclass
class Alert:
    """
    Represents an alert for a medicine.
    
    Attributes:
        medicine: The medicine associated with the alert
        alert_type: Type of the alert
        message: Human-readable alert message
        severity: Severity level (1=low, 3=high)
    """
    medicine: Medicine
    alert_type: AlertType
    message: str
    severity: int  # 1 = low, 2 = medium, 3 = high


class AlertSystem:
    """
    System for monitoring inventory and generating alerts.
    
    Monitors for:
    - Expired medicines
    - Medicines expiring within threshold
    - Low stock items
    - Out of stock items
    
    Attributes:
        expiry_threshold: Days before expiry to trigger alert (default: 30)
        low_stock_threshold: Quantity threshold for low stock (default: 5)
    """
    
    def __init__(
        self,
        expiry_threshold: int = 30,
        low_stock_threshold: int = 5
    ):
        """
        Initialize AlertSystem with thresholds.
        
        Args:
            expiry_threshold: Days before expiry to trigger alert
            low_stock_threshold: Quantity below which to trigger alert
        """
        self.expiry_threshold = expiry_threshold
        self.low_stock_threshold = low_stock_threshold
    
    def check_expiry(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Find medicines that are expired or expiring soon.
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            List of medicines with days_until_expiry <= threshold,
            sorted by expiry date (soonest first)
        """
        expiring = [
            med for med in medicines
            if med.days_until_expiry() <= self.expiry_threshold
        ]
        
        # Sort by expiry date (soonest first)
        expiring.sort(key=lambda m: m.expiry_date)
        
        return expiring
    
    def check_low_stock(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Find medicines with low stock levels.
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            List of medicines with quantity <= threshold,
            sorted by quantity (lowest first)
        """
        low_stock = [
            med for med in medicines
            if med.quantity <= self.low_stock_threshold
        ]
        
        # Sort by quantity (lowest first)
        low_stock.sort(key=lambda m: m.quantity)
        
        return low_stock
    
    def check_expired(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Find already expired medicines.
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            List of expired medicines (expiry_date < today),
            sorted by expiry date (oldest first)
        """
        expired = [med for med in medicines if med.is_expired()]
        
        # Sort by expiry date (oldest first - most overdue)
        expired.sort(key=lambda m: m.expiry_date)
        
        return expired
    
    def check_out_of_stock(self, medicines: List[Medicine]) -> List[Medicine]:
        """
        Find medicines that are completely out of stock.
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            List of medicines with quantity == 0, sorted by name
        """
        out_of_stock = [med for med in medicines if med.quantity == 0]
        
        # Sort by name for easy reference
        out_of_stock.sort(key=lambda m: m.name)
        
        return out_of_stock
    
    def generate_alerts(self, medicines: List[Medicine]) -> List[Alert]:
        """
        Generate all alerts for a list of medicines.
        
        Checks for:
        - Expired medicines (severity: 3)
        - Expiring soon (severity: 2)
        - Out of stock (severity: 3)
        - Low stock (severity: 1)
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            List of Alert objects, sorted by severity (highest first)
        """
        alerts: List[Alert] = []
        
        # Check for expired medicines (highest priority)
        for med in self.check_expired(medicines):
            days_overdue = abs(med.days_until_expiry())
            alerts.append(Alert(
                medicine=med,
                alert_type=AlertType.EXPIRED,
                message=f"'{med.name}' đã hết hạn {days_overdue} ngày",
                severity=3
            ))
        
        # Check for expiring soon (exclude already expired)
        for med in self.check_expiry(medicines):
            if not med.is_expired():
                days_left = med.days_until_expiry()
                alerts.append(Alert(
                    medicine=med,
                    alert_type=AlertType.EXPIRING_SOON,
                    message=f"'{med.name}' sẽ hết hạn trong {days_left} ngày",
                    severity=2
                ))
        
        # Check for out of stock (highest priority)
        for med in self.check_out_of_stock(medicines):
            alerts.append(Alert(
                medicine=med,
                alert_type=AlertType.OUT_OF_STOCK,
                message=f"'{med.name}' đã hết hàng",
                severity=3
            ))
        
        # Check for low stock (exclude out of stock - already handled)
        for med in self.check_low_stock(medicines):
            if med.quantity > 0:
                alerts.append(Alert(
                    medicine=med,
                    alert_type=AlertType.LOW_STOCK,
                    message=f"'{med.name}' còn ít hàng ({med.quantity} đơn vị)",
                    severity=1
                ))
        
        # Sort by severity (highest first)
        alerts.sort(key=lambda a: a.severity, reverse=True)
        
        return alerts
    
    def get_alert_summary(self, medicines: List[Medicine]) -> dict:
        """
        Get summary statistics for alerts.
        
        Args:
            medicines: List of medicines to check
            
        Returns:
            Dictionary with counts for each alert type
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
