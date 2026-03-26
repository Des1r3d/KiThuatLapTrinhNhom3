import sys
import os
from PyQt6 import QtWidgets, uic


class MedicineDetailDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Lấy đường dẫn tuyệt đối để tránh lỗi FileNotFoundError
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "thong_tin_thuoc_dark.ui")  # Thay tên file của bạn vào đây

        # Load giao diện
        uic.loadUi(ui_path, self)

        # Ví dụ kết nối nút bấm (dựa trên objectName trong XML của bạn)
        self.btn_primary.clicked.connect(self.on_edit)
        self.btn_secondary.clicked.connect(self.on_delete)

    def on_edit(self):
        print("Đang mở màn hình chỉnh sửa...")

    def on_delete(self):
        print("Xác nhận xóa thuốc này?")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MedicineDetailDialog()
    window.show()
    sys.exit(app.exec())