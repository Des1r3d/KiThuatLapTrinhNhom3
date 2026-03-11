import sys
import os
from PyQt6 import QtWidgets, uic, QtCore, QtGui


class SuccessDialog(QtWidgets.QDialog):
    def __init__(self, medicine_code="K-A1.001"):
        super().__init__()

        # 1. Load file .ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "xoa_thanh_cong.ui")
        uic.loadUi(ui_path, self)

        # 2. Cấu hình bo góc mượt (Bắt buộc phải có)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # 3. Đổ dữ liệu động
        self.lbl_code.setText(f"Mã thuốc: {medicine_code}")

        # 4. Kết nối nút bấm
        self.btn_close.clicked.connect(self.accept)

        # 5. Thêm hiệu ứng Shadow (Đổ bóng) cho khung trắng
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
        self.container_frame.setGraphicsEffect(shadow)

    # Mẹo: Giữ chuột vào bất kỳ đâu trên Dialog để kéo đi
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Chạy thử Dialog
    window = SuccessDialog(medicine_code="K-A1.001")
    window.show()

    sys.exit(app.exec())