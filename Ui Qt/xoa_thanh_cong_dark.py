import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic, QtCore  # Nhớ import thêm QtCore


class TestDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load file UI của bạn
        uic.loadUi('xoa_thanh_cong_dark.ui', self)

        # --- HAI DÒNG QUAN TRỌNG ĐỂ BIẾN THÀNH POP-UP ---
        # 1. Ẩn thanh tiêu đề (Frameless) và đặt nó luôn nổi lên trên (WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # 2. Làm nền của Dialog trong suốt để lộ cái bo góc 20px bạn làm trong XML
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # -----------------------------------------------

        # Kết nối nút "Đóng thông báo"
        if hasattr(self, 'btn_close'):
            self.btn_close.clicked.connect(self.accept)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TestDialog()
    window.show()

    sys.exit(app.exec())