import sys

from Functions.Config import cfg
from Functions.Log import get_logger
from Functions.SignalBus import signalBus
from PySide6.QtCore import Qt, QTranslator, Slot
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
    InfoBar,
    InfoBarPosition,
    NavigationItemPosition,
    SubtitleLabel,
    Theme,
    setFont,
    setTheme,
)
from qfluentwidgets import FluentIcon as FIF
from resources import resources_rc  # noqa: F401
from UI import (
    # CMessageBox,
    HomeInterface,
    ReadAndChatWidget,
    SettingInterface,
)


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
        QFontDatabase.addApplicationFont(":/fonts/Segoe UI.ttf")
        QFontDatabase.addApplicationFont(":/fonts/Segoe UI Semibold.ttf")
        # QFontDatabase.addApplicationFont(":/fonts/MSYH.ttf")
        self.interfaceList = []
        self.home_page = HomeInterface(self)
        self.read_page = ReadAndChatWidget(self)

        # for i in range(0, 12):
        #     message_label1 = CMessageBox(":/images/github_rebot.png", "Rebot", self)
        #     message_label1.setMessageText(
        #         "This is a test message, it's helpful to dev new function avoid input ever time"
        #     )
        #     self.read_page.chat_widget.messages_list.addWidget(message_label1)

        self.setting_page = SettingInterface(self)

        self.interfaceList.append(self.home_page)
        self.interfaceList.append(self.read_page)
        self.interfaceList.append(self.setting_page)

        self.initNavigation()
        self.initWindow()
        self.connectSignalToSlot()

    def initNavigation(self):
        self.addSubInterface(self.home_page, FIF.HOME, self.tr("Home"))
        self.addSubInterface(self.read_page, FIF.CHAT, self.tr("Read with LLM"))

        self.addSubInterface(
            self.setting_page,
            FIF.SETTING,
            self.tr("Settings"),
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(1000, 800)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)

        self.setMicaEffectEnabled(cfg.get(cfg.mica_enabled))

    def connectSignalToSlot(self):
        signalBus.switch_page_signal.connect(self.switchPage)
        signalBus.info_signal.connect(self.showInfoMessage)
        signalBus.warning_signal.connect(self.showWarningMessage)
        signalBus.error_signal.connect(self.showErrorMessage)

        signalBus.mica_enable_change_signal.connect(self.setMicaEffectEnabled)

    @Slot(str)
    def switchPage(self, page_name: str):
        for w in self.interfaceList:
            if w.objectName() == page_name:
                self.stackedWidget.setCurrentWidget(w, False)

    @Slot(str)
    def showInfoMessage(self, info_message: str):
        InfoBar.info(
            title="INFO",
            content=info_message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )

    @Slot(str)
    def showWarningMessage(self, warning_message: str):
        InfoBar.warning(
            title="WARN",
            content=warning_message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )

    @Slot(str)
    def showErrorMessage(self, error_message: str):
        print("test: ", error_message)
        InfoBar.error(
            title="Error",
            content=error_message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )


def main():
    logger = get_logger("main")
    logger.info("start application...")
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

    logger.info("start finish...")
    app.exec()
