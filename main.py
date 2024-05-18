import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow, InfoBadge, InfoBadgePosition

import resources  # noqa: F401
import src  # noqa: F401
from UI import ChatWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.home_page = ChatWidget(self)
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.home_page, FIF.HOME, "Home")

        # item = self.navigationInterface.widget(self.videoInterface.objectName())
        # InfoBadge.attension(
        #     text=9,
        #     parent=item.parent(),
        #     target=item,
        #     position=InfoBadgePosition.NAVIGATION_ITEM,
        # )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
