import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    FluentWindow,
    Theme,
    setTheme,
)

import resources  # noqa: F401
import src  # noqa: F401
from UI import ChatWidget, MessageBox


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.home_page = ChatWidget(self)
        for i in range(0, 10):
            message_label1 = MessageBox(":/title/github.png", "User", self)
            message_label1.setMessageText(
                "This is a test message, it's helpful to dev new function avoid input ever time"
            )
            self.home_page.messages_list.addWidget(message_label1)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.home_page, FIF.HOME, "Home")

        # item = self.navigationInterface.widget(self.videoInterface.objectName())
        # InfoBadge.attension(
        #     text=9,
        #     parent=item.parent(),
        #     target=item,
        #     position=InfoBadgePosition.NAVIGATION_ITEM,
        # )

    def initWindow(self):
        self.resize(900, 700)


def main():
    setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
