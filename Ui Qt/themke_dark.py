import sys
import os
from PyQt6 import QtWidgets, uic, QtGui


class AddShelfDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # 1. Load file .ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "them_ke_dark.ui")  # Đảm bảo tên file .ui của bạn trùng ở đây
        uic.loadUi(ui_path, self)

        # 2. Ràng buộc dữ liệu (Chỉ cho nhập số vào ô Sức chứa)
        # Giới hạn từ 1 đến 9999
        validator = QtGui.QIntValidator(1, 9999, self)
        self.txt_shelf_capacity.setValidator(validator)

        # 3. Kết nối nút bấm
        self.btn_primary.clicked.connect(self.save_shelf)  # Nút Save
        self.btn_secondary.clicked.connect(self.reject)  # Nút Cancel

    def save_shelf(self):
        # Lấy dữ liệu từ các ô nhập
        shelf_id = self.txt_shelf_id.text()
        row = self.txt_shelf_row.text()
        col = self.txt_shelf_col.text()
        capacity = self.txt_shelf_capacity.text()

        # Kiểm tra nhanh xem đã nhập đủ chưa
        if not shelf_id or not capacity:
            QtWidgets.QMessageBox.warning(self, "Chú ý", "Bạn vui lòng nhập đầy đủ ID và Sức chứa nha!")
            return

        print(f"--- Đã lưu kệ mới ---")
        print(f"ID: {shelf_id}")
        print(f"Vị trí: Dãy {row} - Cột {col}")
        print(f"Sức chứa: {capacity}")

        QtWidgets.QMessageBox.information(self, "Thành công", f"Đã thêm kệ {shelf_id} vào hệ thống!")
        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddShelfDialog()
    window.show()
    sys.exit(app.exec())