import sys

from MainWindow import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        text = self.lineEdit.text()
        print(text)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
