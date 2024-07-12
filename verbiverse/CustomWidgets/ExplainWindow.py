from CustomWidgets.StyleSheet import StyleSheet
from ExplainWindow_ui import Ui_ExplainWindow
from Functions.SignalBus import signalBus
from Functions.WordBookDatabase import WordsBookDatabase
from ModuleLogger import logger
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon as FIF


class ExplainWindow(QWidget, Ui_ExplainWindow):
    close_signal = Signal()

    def __init__(
        self, title, content, resource="", already_add=False, parent: QWidget = None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedWidth(550)

        self.title = title
        self.content = content
        self.resource = resource
        self.title_label.setText(title)
        self.content_label.setText(content)

        self.close_button.setIcon(FIF.CLOSE)
        self.close_button.setFixedSize(32, 32)
        self.close_button.setIconSize(QSize(12, 12))

        self.add_button.setIcon(FIF.ADD)
        self.add_button.setFixedSize(32, 32)
        self.add_button.setIconSize(QSize(12, 12))
        self.add_button.clicked.connect(self.addWord)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.close_button.clicked.connect(self.closeWindow)

        StyleSheet.EXPLAIN_WINDOW.apply(self)

    def addWord(self):
        db = WordsBookDatabase()
        if not db.parseExplainAndAddWords(self.title, self.content, self.resource):
            logger.error(f"add word error: {self.title}")
        else:
            signalBus.info_signal("add word success: %s" % self.title)

        self.add_button.setEnabled(False)

    def closeWindow(self):
        self.close_signal.emit()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        event.accept()

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content
        self.content_label.setText(self.content)
        # self.adjustSize()
