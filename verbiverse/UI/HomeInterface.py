from CustomWidgets import LinkCardView, StyleSheet
from Functions.Config import REPO_URL
from Functions.SignalBus import signalBus
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon, ScrollArea, isDarkTheme

# from ..common.icon import Icon, FluentIconBase
# from ..components.link_card import LinkCardView
# from ..components.sample_card import SampleCardView
# from ..common.style_sheet import StyleSheet


class BannerWidget(QWidget):
    """Banner widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.verbiverse_label = QLabel("Verbiverse", self)
        self.banner = QPixmap(":/images/banner_1920.png")
        self.link_card_view = LinkCardView(self)

        self.verbiverse_label.setObjectName("verbiverse_label")

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)

        self.vBoxLayout.addWidget(self.verbiverse_label)
        self.vBoxLayout.addWidget(self.link_card_view, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.link_card_view.addButtonCard(
            FluentIcon.LIBRARY,
            self.tr("Getting started"),
            self.tr("Open a local pdf file."),
            self.callback,
            "ReadAndChatWidget",
        )
        self.link_card_view.addCard(
            FluentIcon.GITHUB,
            self.tr("GitHub repo"),
            self.tr("Check."),
            REPO_URL,
        )

    def callback(self, args):
        signalBus.switch_page_signal.emit(args)

    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("homeInterface")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """load samples"""
        pass