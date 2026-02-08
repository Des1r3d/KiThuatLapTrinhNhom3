"""
Test suite for AlertSystem.
Tests cover expiry alerts, low stock alerts, and alert generation.
"""
import pytest
from datetime import date, timedelta
from src.models import Medicine
from src.alerts import AlertSystem, AlertType, Alert


class TestAlertSystem:
    """Test suite for AlertSystem class."""
    
    @pytest.fixture
    def alert_system(self):
        """Create AlertSystem with default thresholds."""
        return AlertSystem(expiry_threshold=30, low_stock_threshold=5)
    
    @pytest.fixture
    def expired_medicine(self):
        """Create an expired medicine."""
        return Medicine(
            id="MED001",
            name="Expired Medicine",
            quantity=10,
            expiry_date=date.today() - timedelta(days=5),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    @pytest.fixture
    def expiring_medicine(self):
        """Create a medicine expiring within threshold."""
        return Medicine(
            id="MED002",
            name="Expiring Soon",
            quantity=10,
            expiry_date=date.today() + timedelta(days=15),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    @pytest.fixture
    def valid_medicine(self):
        """Create a valid medicine (not expiring soon)."""
        return Medicine(
            id="MED003",
            name="Valid Medicine",
            quantity=100,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    @pytest.fixture
    def low_stock_medicine(self):
        """Create a low stock medicine."""
        return Medicine(
            id="MED004",
            name="Low Stock",
            quantity=3,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    @pytest.fixture
    def out_of_stock_medicine(self):
        """Create an out of stock medicine."""
        return Medicine(
            id="MED005",
            name="Out of Stock",
            quantity=0,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
    
    # === Initialization Tests ===
    
    def test_default_thresholds(self):
        """Test default threshold values."""
        system = AlertSystem()
        
        assert system.expiry_threshold == 30
        assert system.low_stock_threshold == 5
    
    def test_custom_thresholds(self):
        """Test custom threshold values."""
        system = AlertSystem(expiry_threshold=60, low_stock_threshold=10)
        
        assert system.expiry_threshold == 60
        assert system.low_stock_threshold == 10
    
    # === Check Expiry Tests ===
    
    def test_check_expiry_returns_expiring_medicines(
        self, alert_system, expired_medicine, expiring_medicine, valid_medicine
    ):
        """Test check_expiry returns medicines within threshold."""
        medicines = [expired_medicine, expiring_medicine, valid_medicine]
        
        result = alert_system.check_expiry(medicines)
        
        assert len(result) == 2
        assert expired_medicine in result
        assert expiring_medicine in result
        assert valid_medicine not in result
    
    def test_check_expiry_sorted_by_date(
        self, alert_system, expired_medicine, expiring_medicine
    ):
        """Test check_expiry returns results sorted by expiry date."""
        medicines = [expiring_medicine, expired_medicine]  # Reverse order
        
        result = alert_system.check_expiry(medicines)
        
        # Expired should come first (soonest expiry)
        assert result[0] == expired_medicine
        assert result[1] == expiring_medicine
    
    def test_check_expiry_empty_list(self, alert_system):
        """Test check_expiry with empty list."""
        result = alert_system.check_expiry([])
        
        assert result == []
    
    def test_check_expiry_boundary_condition(self, alert_system):
        """Test check_expiry with medicine expiring exactly at threshold."""
        medicine = Medicine(
            id="MED001",
            name="At Threshold",
            quantity=10,
            expiry_date=date.today() + timedelta(days=30),
            shelf_id="SHELF-A1",
            price=5.99
        )
        
        result = alert_system.check_expiry([medicine])
        
        assert len(result) == 1
        assert medicine in result
    
    # === Check Expired Tests ===
    
    def test_check_expired_returns_only_expired(
        self, alert_system, expired_medicine, expiring_medicine, valid_medicine
    ):
        """Test check_expired returns only expired medicines."""
        medicines = [expired_medicine, expiring_medicine, valid_medicine]
        
        result = alert_system.check_expired(medicines)
        
        assert len(result) == 1
        assert expired_medicine in result
    
    def test_check_expired_includes_today(self, alert_system):
        """Test check_expired includes medicines expiring today."""
        medicine = Medicine(
            id="MED001",
            name="Expires Today",
            quantity=10,
            expiry_date=date.today(),
            shelf_id="SHELF-A1",
            price=5.99
        )
        
        result = alert_system.check_expired([medicine])
        
        assert len(result) == 1
    
    # === Check Low Stock Tests ===
    
    def test_check_low_stock_returns_low_quantity(
        self, alert_system, low_stock_medicine, valid_medicine
    ):
        """Test check_low_stock returns medicines below threshold."""
        medicines = [low_stock_medicine, valid_medicine]
        
        result = alert_system.check_low_stock(medicines)
        
        assert len(result) == 1
        assert low_stock_medicine in result
    
    def test_check_low_stock_sorted_by_quantity(self, alert_system, out_of_stock_medicine, low_stock_medicine):
        """Test check_low_stock returns results sorted by quantity."""
        medicines = [low_stock_medicine, out_of_stock_medicine]
        
        result = alert_system.check_low_stock(medicines)
        
        # Out of stock (0) should come first
        assert result[0] == out_of_stock_medicine
        assert result[1] == low_stock_medicine
    
    def test_check_low_stock_boundary_condition(self, alert_system):
        """Test check_low_stock with medicine exactly at threshold."""
        medicine = Medicine(
            id="MED001",
            name="At Threshold",
            quantity=5,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
        
        result = alert_system.check_low_stock([medicine])
        
        assert len(result) == 1
    
    # === Check Out of Stock Tests ===
    
    def test_check_out_of_stock(
        self, alert_system, out_of_stock_medicine, low_stock_medicine, valid_medicine
    ):
        """Test check_out_of_stock returns only zero quantity."""
        medicines = [out_of_stock_medicine, low_stock_medicine, valid_medicine]
        
        result = alert_system.check_out_of_stock(medicines)
        
        assert len(result) == 1
        assert out_of_stock_medicine in result
    
    def test_check_out_of_stock_sorted_by_name(self, alert_system):
        """Test check_out_of_stock returns results sorted by name."""
        med1 = Medicine(
            id="MED001",
            name="Zebra Medicine",
            quantity=0,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
        med2 = Medicine(
            id="MED002",
            name="Alpha Medicine",
            quantity=0,
            expiry_date=date.today() + timedelta(days=365),
            shelf_id="SHELF-A1",
            price=5.99
        )
        
        result = alert_system.check_out_of_stock([med1, med2])
        
        assert result[0] == med2  # Alpha first
        assert result[1] == med1  # Zebra second
    
    # === Generate Alerts Tests ===
    
    def test_generate_alerts_expired(self, alert_system, expired_medicine):
        """Test generate_alerts creates alert for expired medicine."""
        result = alert_system.generate_alerts([expired_medicine])
        
        assert len(result) == 1
        assert result[0].alert_type == AlertType.EXPIRED
        assert result[0].severity == 3
        assert "hết hạn" in result[0].message
    
    def test_generate_alerts_expiring_soon(self, alert_system, expiring_medicine):
        """Test generate_alerts creates alert for expiring medicine."""
        result = alert_system.generate_alerts([expiring_medicine])
        
        assert len(result) == 1
        assert result[0].alert_type == AlertType.EXPIRING_SOON
        assert result[0].severity == 2
    
    def test_generate_alerts_low_stock(self, alert_system, low_stock_medicine):
        """Test generate_alerts creates alert for low stock."""
        result = alert_system.generate_alerts([low_stock_medicine])
        
        assert len(result) == 1
        assert result[0].alert_type == AlertType.LOW_STOCK
        assert result[0].severity == 1
    
    def test_generate_alerts_out_of_stock(self, alert_system, out_of_stock_medicine):
        """Test generate_alerts creates alert for out of stock."""
        result = alert_system.generate_alerts([out_of_stock_medicine])
        
        assert len(result) == 1
        assert result[0].alert_type == AlertType.OUT_OF_STOCK
        assert result[0].severity == 3
    
    def test_generate_alerts_sorted_by_severity(
        self, alert_system, expired_medicine, expiring_medicine, low_stock_medicine
    ):
        """Test generate_alerts returns alerts sorted by severity."""
        medicines = [low_stock_medicine, expiring_medicine, expired_medicine]
        
        result = alert_system.generate_alerts(medicines)
        
        # Check severity order (3, 2, 1)
        for i in range(len(result) - 1):
            assert result[i].severity >= result[i + 1].severity
    
    def test_generate_alerts_no_duplicates_for_expired(
        self, alert_system, expired_medicine
    ):
        """Test that expired medicine doesn't also appear as expiring soon."""
        result = alert_system.generate_alerts([expired_medicine])
        
        # Should only have EXPIRED alert, not EXPIRING_SOON
        alert_types = [a.alert_type for a in result]
        assert AlertType.EXPIRED in alert_types
        assert AlertType.EXPIRING_SOON not in alert_types
    
    def test_generate_alerts_no_duplicates_for_out_of_stock(
        self, alert_system, out_of_stock_medicine
    ):
        """Test that out of stock doesn't also appear as low stock."""
        result = alert_system.generate_alerts([out_of_stock_medicine])
        
        # Should only have OUT_OF_STOCK alert, not LOW_STOCK
        alert_types = [a.alert_type for a in result]
        assert AlertType.OUT_OF_STOCK in alert_types
        assert AlertType.LOW_STOCK not in alert_types
    
    def test_generate_alerts_valid_medicine_no_alerts(
        self, alert_system, valid_medicine
    ):
        """Test that valid medicine generates no alerts."""
        result = alert_system.generate_alerts([valid_medicine])
        
        assert len(result) == 0
    
    # === Get Alert Summary Tests ===
    
    def test_get_alert_summary(
        self, alert_system, expired_medicine, expiring_medicine,
        out_of_stock_medicine, low_stock_medicine, valid_medicine
    ):
        """Test get_alert_summary returns correct counts."""
        medicines = [
            expired_medicine, expiring_medicine,
            out_of_stock_medicine, low_stock_medicine, valid_medicine
        ]
        
        summary = alert_system.get_alert_summary(medicines)
        
        assert summary["expired"] == 1
        assert summary["expiring_soon"] == 1  # Only expiring_medicine (not expired)
        assert summary["out_of_stock"] == 1
        assert summary["low_stock"] == 1  # Only low_stock (not out_of_stock)
        assert summary["total_medicines"] == 5
    
    def test_get_alert_summary_empty(self, alert_system):
        """Test get_alert_summary with empty list."""
        summary = alert_system.get_alert_summary([])
        
        assert summary["expired"] == 0
        assert summary["expiring_soon"] == 0
        assert summary["out_of_stock"] == 0
        assert summary["low_stock"] == 0
        assert summary["total_medicines"] == 0


class TestAlert:
    """Test suite for Alert dataclass."""
    
    def test_alert_creation(self):
        """Test creating an Alert object."""
        medicine = Medicine(
            id="MED001",
            name="Test Medicine",
            quantity=10,
            expiry_date=date.today() - timedelta(days=5),
            shelf_id="SHELF-A1",
            price=5.99
        )
        
        alert = Alert(
            medicine=medicine,
            alert_type=AlertType.EXPIRED,
            message="Test medicine đã hết hạn 5 ngày",
            severity=3
        )
        
        assert alert.medicine == medicine
        assert alert.alert_type == AlertType.EXPIRED
        assert alert.message == "Test medicine đã hết hạn 5 ngày"
        assert alert.severity == 3


class TestAlertType:
    """Test suite for AlertType enum."""
    
    def test_alert_types_exist(self):
        """Test all expected alert types exist."""
        assert AlertType.EXPIRED.value == "expired"
        assert AlertType.EXPIRING_SOON.value == "expiring_soon"
        assert AlertType.LOW_STOCK.value == "low_stock"
        assert AlertType.OUT_OF_STOCK.value == "out_of_stock"
