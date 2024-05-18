import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QPixmap
from PySide6.QtWidgets import QApplication, QFrame

import resources  # noqa: F401
import src  # noqa: F401
from UI import Ui_MessageBox


class MainWindow(QFrame, Ui_MessageBox):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.setupUi(self)
        # self.user_image.setRadius(12)

        pixmap = QPixmap(":/title/github.png").scaled(
            self.user_image.size() / 4,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        self.user_image.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
