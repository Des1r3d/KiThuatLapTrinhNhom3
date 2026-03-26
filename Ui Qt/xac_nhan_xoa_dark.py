import sys
import os
from PyQt6 import QtWidgets, uic, QtCore


class ConfirmDeleteDialog(QtWidgets.QDialog):
    def __init__(self, medicine_name="Paracetamol 500mg", medicine_code="K-A1.001", qty=150):
        super().__init__()

        # 1. Load file .ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "xac_nhan_xoa_dark.ui")
        uic.loadUi(ui_path, self)

        # 2. Cấu hình để bo góc mượt mà (Bắt buộc phải có)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # 3. Đổ dữ liệu động vào (Team code sẽ làm phần này)
        self.lbl_title.setText(f"XÁC NHẬN XOÁ\n{medicine_name.upper()}")
        self.lbl_qty.setText(f"SỐ LƯỢNG: {qty}")
        self.lbl_code.setText(f"Mã thuốc: {medicine_code}")

        # 4. Kết nối nút bấm
        self.btn_delete.clicked.connect(self.accept)  # Trả về kết quả Xác nhận
        self.btn_cancel.clicked.connect(self.reject)  # Trả về kết quả Hủy

        # Thêm hiệu ứng Shadow (Đổ bóng) cho sang chảnh
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 50))
        self.container_frame.setGraphicsEffect(shadow)

    # Mẹo: Cho phép nhấn giữ chuột vào vùng trống để kéo Dialog đi chỗ khác
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


if __name__ == "__main__":
    from PyQt6 import QtGui  # Import thêm để dùng QColor cho Shadow

    app = QtWidgets.QApplication(sys.argv)

    # Giả sử test với một loại thuốc cụ thể
    window = ConfirmDeleteDialog(
        medicine_name="Paracetamol 500mg",
        medicine_code="K-A1.001",
        qty=150
    )

    # Hiển thị và kiểm tra kết quả bấm nút
    if window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        print("Hệ thống: Đang thực hiện lệnh xóa...")
    else:
        print("Hệ thống: Đã hủy lệnh xóa.")

    sys.exit()