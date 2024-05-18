import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

import resources  # noqa: F401
import src  # noqa: F401
from UI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
