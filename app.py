"""
Pharmacy Management System - Main Application Entry Point

A comprehensive pharmacy inventory management system with:
- Medicine CRUD operations
- Expiry and stock monitoring
- Fuzzy search
- Dark/Light theme
- Dashboard with charts

Usage:
    python app.py
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.ui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Pharmacy Management System")
    app.setOrganizationName("KiThuatLapTrinhNhom3")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
