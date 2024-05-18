import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QFrame

import resources  # noqa: F401
import src  # noqa: F401
from UI import Ui_MessageBox


class MainWindow(QFrame, Ui_MessageBox):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.setupUi(self)
        self.user_image.setImage(":/title/github.png")
        self.user_image.scaledToHeight(30)
        self.user_image.setBorderRadius(8, 8, 8, 8)
        self.user_name.setText("BOT")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
