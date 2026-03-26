import sys
import os
from PyQt6 import QtWidgets, uic


class AddMedicineDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Load file .ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "them_thuoc_dark.ui")
        uic.loadUi(ui_path, self)

        # 1. Thiết lập dữ liệu mẫu cho ComboBox (Kệ thuốc)
        self.setup_combobox()

        # 2. Kết nối các nút bấm (Theo objectName trong XML)
        self.btn_primary.clicked.connect(self.save_data)  # Nút Save
        self.btn_secondary.clicked.connect(self.close)  # Nút Cancel
        self.btn_add_img.clicked.connect(self.upload_image)  # Nút Thêm ảnh

    def setup_combobox(self):
        # Xóa item mặc định và thêm danh sách kệ thật
        self.cb_shelf_location.clear()
        self.cb_shelf_location.addItems(["Chọn kệ thuốc", "Kệ A-01", "Kệ A-02", "Kệ B-05", "Kho Lạnh"])

    def upload_image(self):
        # Mở hộp thoại chọn file ảnh
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Chọn hình ảnh thuốc", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            print(f"Đã chọn ảnh: {file_path}")
            # Sau này bạn có thể dùng QPixmap để hiển thị ảnh lên khung upload

    def save_data(self):
        # Lấy dữ liệu từ các ô nhập (Theo đúng Naming Convention của bạn)
        data = {
            "ID": self.txt_medicine_id.text(),
            "Tên": self.txt_medicine_name.text(),
            "Số lượng": self.txt_quantity.text(),
            "HSD": self.txt_expiry_date.text(),
            "Kệ": self.cb_shelf_location.currentText(),
            "Giá": self.txt_price.text()
        }

        print("Dữ liệu chuẩn bị lưu:")
        for key, value in data.items():
            print(f"- {key}: {value}")

        QtWidgets.QMessageBox.information(self, "Thành công", "Đã lưu thông tin thuốc mới!")
        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddMedicineDialog()
    window.show()
    sys.exit(app.exec())