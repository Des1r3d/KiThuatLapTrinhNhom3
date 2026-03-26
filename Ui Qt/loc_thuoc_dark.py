import sys
import os
from PyQt6 import QtWidgets, uic


class FilterMedicineDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # 1. Load file .ui (Đảm bảo tên file trùng với file bạn lưu)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "loc_thuoc_dark.ui")  # Đổi tên này nếu bạn đặt tên khác
        uic.loadUi(ui_path, self)

        # 2. Nạp dữ liệu vào các ComboBox
        self.init_combobox_data()

        # 3. Kết nối nút bấm
        self.btn_primary.clicked.connect(self.apply_filter)  # Nút Save
        self.btn_secondary.clicked.connect(self.reject)  # Nút Cancel

    def init_combobox_data(self):
        # Nạp Mã kệ
        self.cb_filter_shelf.addItems(["Kệ A-01", "Kệ A-02", "Kệ B-01", "Kệ B-02"])

        # Nạp Khoảng giá
        self.cb_filter_price.addItems([
            "Dưới 50.000đ",
            "50.000đ - 200.000đ",
            "Trên 200.000đ"
        ])

        # Nạp Trạng thái
        self.cb_filter_status.addItems(["Tất cả", "Còn hàng", "Hết hạn", "Sắp hết hạn"])

    def apply_filter(self):
        # Lấy giá trị người dùng chọn
        shelf = self.cb_filter_shelf.currentText()
        price = self.cb_filter_price.currentText()
        status = self.cb_filter_status.currentText()

        print(f"--- Đã áp dụng bộ lọc ---")
        print(f"Kệ: {shelf}")
        print(f"Giá: {price}")
        print(f"Trạng thái: {status}")

        # Sau khi lọc xong thì đóng cửa sổ
        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FilterMedicineDialog()
    window.show()
    sys.exit(app.exec())