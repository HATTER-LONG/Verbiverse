import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
)
from qfluentwidgets import (
    FluentBackgroundTheme,
    FluentWindow,
    Theme,
    setTheme,
)
from qfluentwidgets import FluentIcon as FIF

import resources  # noqa: F401
import src  # noqa: F401
from UI import MessageBox, ReadAndChatWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.home_page = ReadAndChatWidget(self)
        for i in range(0, 15):
            message_label1 = MessageBox(":/title/github.png", "User", self)
            message_label1.setMessageText(
                "This is a test message, it's helpful to dev new function avoid input ever time"
            )
            self.home_page.chat_widget.messages_list.addWidget(message_label1)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.home_page, FIF.HOME, "Home")

    def initWindow(self):
        self.resize(1000, 800)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)


def main():
    setTheme(Theme.LIGHT)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
