import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
)
from qfluentwidgets import (
    FluentBackgroundTheme,
    FluentTranslator,
    FluentWindow,
    NavigationItemPosition,
    SubtitleLabel,
    Theme,
    setFont,
    setTheme,
)
from qfluentwidgets import FluentIcon as FIF

import resources  # noqa: F401
from src.Functions.Config import cfg
from UI import CMessageBox, ReadAndChatWidget, SettingInterface


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(" ", "-"))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")
        self.home_page = Widget("Home", self)
        self.read_page = ReadAndChatWidget(self)

        for i in range(0, 15):
            message_label1 = CMessageBox(":/title/github.png", "User", self)
            message_label1.setMessageText(
                "This is a test message, it's helpful to dev new function avoid input ever time"
            )
            self.read_page.chat_widget.messages_list.addWidget(message_label1)

        self.setting_page = SettingInterface(self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.home_page, FIF.HOME, "Home")
        self.addSubInterface(self.read_page, FIF.CHAT, "Read & Chat")

        self.addSubInterface(
            self.setting_page,
            FIF.SETTING,
            self.tr("Settings"),
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(1000, 800)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)


def main():
    setTheme(Theme.LIGHT)

    app = QApplication(sys.argv)

    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    galleryTranslator.load(locale, "verbiverse", ".", ":/i18n")

    app.installTranslator(translator)
    app.installTranslator(galleryTranslator)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
