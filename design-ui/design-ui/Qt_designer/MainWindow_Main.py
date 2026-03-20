import sys
from MainWindow_ext import MainWindow_ext
from PyQt6.QtWidgets import QApplication
app=QApplication(sys.argv)

w=MainWindow_ext()
w.show()



sys.exit(app.exec())