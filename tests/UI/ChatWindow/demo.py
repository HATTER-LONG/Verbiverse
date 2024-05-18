import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QFrame

import resources  # noqa: F401
import src  # noqa: F401
from UI import Ui_ChatWindow


class MainWindow(QFrame, Ui_ChatWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")

        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
