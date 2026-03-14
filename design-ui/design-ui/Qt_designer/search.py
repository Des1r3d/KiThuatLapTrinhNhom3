import sys
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from difflib import SequenceMatcher


class SearchDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("search.ui", self)

        # Danh sách thuốc mẫu trong database
        self.medicine_db = [
            {"name": "Paracetamol 500mg", "shelf": "K-A1"},
            {"name": "Cetirizine 10mg", "shelf": "K-B2"},
            {"name": "Vitamin C 1000mg", "shelf": "K-B1"}
        ]

        # Khi gõ chữ thì tự động tìm kiếm
        self.txt_search.textChanged.connect(self.perform_search)
        self.perform_search("")  # Hiện tất cả lúc đầu

    def calculate_match(self, search_text, target_text):
        # Thuật toán tính % độ khớp
        ratio = SequenceMatcher(None, search_text.lower(), target_text.lower()).ratio()
        # Nếu search_text nằm trong target_text thì cộng thêm điểm ưu tiên
        if search_text.lower() in target_text.lower():
            ratio = max(ratio, 0.8)
        return int(ratio * 100)

    def perform_search(self, text):
        self.list_results.clear()
        results = []

        for med in self.medicine_db:
            score = self.calculate_match(text, med['name']) if text else 100
            if score > 20:  # Chỉ hiện kết quả có độ khớp trên 20%
                results.append((med, score))

        # Sắp xếp: Cái nào khớp nhất (%) hiện lên đầu
        results.sort(key=lambda x: x[1], reverse=True)

        for med, score in results:
            self.add_item_to_list(med['name'], med['shelf'], score)

    def add_item_to_list(self, name, shelf, score):
        item_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(item_widget)
        layout.setContentsMargins(20, 15, 20, 15)

        # Màu sắc theo độ khớp
        color = "#16A34A" if score >= 80 else "#D97706" if score >= 50 else "#DC2626"

        info_layout = QtWidgets.QVBoxLayout()
        lbl_name = QtWidgets.QLabel(f"<b>{name}</b>")
        lbl_name.setStyleSheet("font-size: 15px; color: #1E293B; border: none;")
        lbl_shelf = QtWidgets.QLabel(shelf)
        lbl_shelf.setStyleSheet("font-size: 12px; color: #94A3B8; border: none;")
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_shelf)

        lbl_score = QtWidgets.QLabel(f"{score}%")
        lbl_score.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {color}; border: none;")

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(lbl_score)

        list_item = QtWidgets.QListWidgetItem(self.list_results)
        list_item.setSizeHint(item_widget.sizeHint())
        self.list_results.addItem(list_item)
        self.list_results.setItemWidget(list_item, item_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = SearchDialog()
    win.show()
    sys.exit(app.exec())