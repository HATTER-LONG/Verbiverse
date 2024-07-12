from Functions.SignalBus import signalBus
from Functions.WordBookDatabase import WordsBookDatabase
from ModuleLogger import logger
from PySide6.QtCore import QMargins, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import (
    FluentIcon,
    FluentStyleSheet,
    FlyoutViewBase,
    PrimaryToolButton,
    TextWrap,
    TransparentToolButton,
    drawIcon,
)
from qfluentwidgets import FluentIcon as FIF


class IconWidget(QWidget):
    def __init__(self, icon, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(36, 54)
        self.icon = icon

    def paintEvent(self, e):
        if not self.icon:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        rect = QRectF(8, (self.height() - 20) / 2, 20, 20)
        drawIcon(self.icon, painter, rect)


class ExplainFlyoutView(FlyoutViewBase):
    pin_explain_signal = Signal(str, str, bool)

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setFixedWidth(450)
        self.icon = FIF.CHAT.icon()

        self.title = title
        self.content = ""

        self.vBoxLayout = QVBoxLayout(self)
        self.viewLayout = QHBoxLayout()
        self.widgetLayout = QVBoxLayout()

        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(self.content, self)
        # self.contentLabel.setWordWrap(True)
        self.iconWidget = IconWidget(self.icon, self)
        self.pin_button = TransparentToolButton(FluentIcon.PIN, self)

        self.add_button = PrimaryToolButton(FIF.ADD, self)
        self.add_button.clicked.connect(self.addWord)
        self.resource = "None"
        self.already_add = False
        # if self.isSentenceString(self.title):
        #     self.add_button.setEnabled(False)

        self.__initWidgets()

    def __initWidgets(self):
        self.pin_button.setFixedSize(32, 32)
        self.pin_button.setIconSize(QSize(12, 12))
        self.titleLabel.setVisible(bool(self.title))
        # self.contentLabel.setVisible(bool(self.content))

        self.pin_button.clicked.connect(self.pinWindow)

        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        FluentStyleSheet.TEACHING_TIP.apply(self)

        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(1, 1, 1, 1)
        self.widgetLayout.setContentsMargins(0, 8, 0, 8)
        self.viewLayout.setSpacing(4)
        self.widgetLayout.setSpacing(0)
        self.vBoxLayout.setSpacing(0)

        # add icon widget
        if not self.title or not self.content:
            self.iconWidget.setFixedHeight(36)

        self.vBoxLayout.addLayout(self.viewLayout)
        self.vBoxLayout.addWidget(self.add_button, 0, Qt.AlignRight | Qt.AlignBottom)
        self.viewLayout.addWidget(self.iconWidget, 0, Qt.AlignTop)

        # add text
        self._adjustText()
        self.widgetLayout.addWidget(self.titleLabel)
        self.widgetLayout.addWidget(self.contentLabel)
        self.viewLayout.addLayout(self.widgetLayout)

        # add pin button
        self.viewLayout.addWidget(self.pin_button, 0, Qt.AlignRight | Qt.AlignTop)

        # adjust content margins
        margins = QMargins(6, 5, 6, 5)
        margins.setLeft(20 if not self.icon else 5)
        # margins.setRight(20)
        self.viewLayout.setContentsMargins(margins)

    def setTextResource(self, resource: str):
        self.resource = resource
        logger.info("resource: %s" % resource)

    def pinWindow(self):
        self.pin_explain_signal.emit(self.title, self.content, self.already_add)
        self.close()

    def addWord(self):
        db = WordsBookDatabase()
        if not db.parseExplainAndAddWords(self.title, self.content, self.resource):
            logger.error(f"add word error: {self.title}")
            signalBus.error_signal("add word Failed: %s" % self.title)
        else:
            signalBus.info_signal("add word success: %s" % self.title)
            self.already_add = True
        self.add_button.setEnabled(False)

    def addWidget(self, widget: QWidget, stretch=0, align=Qt.AlignLeft):
        """add widget to view"""
        self.widgetLayout.addSpacing(8)
        self.widgetLayout.addWidget(widget, stretch, align)

    def _adjustText(self):
        w = self.width()

        # adjust title
        chars = max(min(w / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        # adjust content
        chars = max(min(w / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

    def showEvent(self, e):
        super().showEvent(e)
        self.adjustSize()

    def setContent(self, content: str):
        self.content = content
        self._adjustText()

    def getContent(self) -> str:
        return self.content
