import sys
import os
from PyQt6 import QtWidgets, uic, QtCore, QtGui


class FullShelfDialog(QtWidgets.QDialog):
    def __init__(self, shelf_id="K-A1.001", capacity=50):
        super().__init__()

        # 1. Load file .ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "ke_day.ui")
        uic.loadUi(ui_path, self)

        # 2. Cấu hình giao diện không viền & trong suốt để thấy bo góc
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # 3. Đổ dữ liệu động (Team code sẽ dùng cái này)
        message = (f"Kệ {shelf_id} hiện tại chỉ còn sức chứa {capacity} đơn vị thuốc. "
                   "Vui lòng chọn kệ khác hoặc thay đổi lượng thuốc nhập vào.")
        self.lbl_desc.setText(message)

        # 4. Kết nối nút bấm
        self.btn_close.clicked.connect(self.accept)

        # 5. Hiệu ứng đổ bóng (Shadow)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 50))
        self.container_frame.setGraphicsEffect(shadow)

    # Cho phép kéo Dialog bằng chuột
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

    # Giả lập tình huống kệ đầy
    window = FullShelfDialog(shelf_id="K-A1.001", capacity=50)
    window.show()

    sys.exit(app.exec())