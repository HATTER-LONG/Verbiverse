from CustomWidgets import CFileListWidget, LinkCardView, StyleSheet
from Functions.Config import REPO_URL
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import (
    QRectF,
    QStandardPaths,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import FluentIcon, ScrollArea, isDarkTheme


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

        self.link_card_view.addButtonCard(
            FluentIcon.VIDEO,
            self.tr("Open Video"),
            self.tr("Open a video file."),
            self.videoFileSelect,
            "VideoInterface",
        )

        self.link_card_view.addCard(
            FluentIcon.GITHUB,
            self.tr("GitHub repo"),
            self.tr("Project homepage."),
            REPO_URL,
        )

        self.m_fileDialog = None
        self.m_videoDialog = None
        signalBus.load_localfile_signal.connect(self.processCall)
        self.process = 0

    # TODO: add process dialogs
    def processCall(self, process: int):
        logger.debug(f"Open local pdf file process: {process}")
        if process == 100:
            signalBus.switch_page_signal.emit("ReadAndChatWidget")

    def callback(self, args):
        if not self.m_fileDialog:
            directory = QStandardPaths.writableLocation(
                QStandardPaths.DocumentsLocation
            )
            self.m_fileDialog = QFileDialog(self, "Choose a PDF", directory)
            self.m_fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            self.m_fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
            self.m_fileDialog.setMimeTypeFilters(["application/pdf"])
        if self.m_fileDialog.exec() == QDialog.Accepted:
            to_open = self.m_fileDialog.selectedUrls()[0]
            if to_open.isValid():
                signalBus.open_localfile_signal.emit(to_open)

    def videoFileSelect(self, args):
        if not self.m_videoDialog:
            directory = QStandardPaths.writableLocation(
                QStandardPaths.DocumentsLocation
            )
            self.m_videoDialog = QFileDialog(self, "Choose a video file", directory)
            self.m_videoDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            self.m_videoDialog.setAcceptMode(QFileDialog.AcceptOpen)
            # self.m_fileDialog.setMimeTypeFilters(["application/pdf"])
        if self.m_videoDialog.exec() == QDialog.Accepted:
            to_open = self.m_videoDialog.selectedUrls()[0]
            if to_open.isValid():
                signalBus.open_video_signal.emit(to_open)

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
        self.file_list = CFileListWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("homeInterface")
        self.file_list.setObjectName("fileList")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.addWidget(self.file_list)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """load samples"""
        pass
