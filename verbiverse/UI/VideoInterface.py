from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import QPoint, Qt, QThread, QUrl, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QFileDialog, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    RoundMenu,
)
from VideoInterface_ui import Ui_VideoInterface


class VideoInterface(QWidget, Ui_VideoInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        signalBus.open_video_signal.connect(self.open)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)
        self.video_widget.player.positionChanged.connect(self.postion)
        self.file_path = None
        self.subtitle_path = None

    def postion(self, time):
        # logger.info(f"set video position: [{self._formatTime(time)}]")

    def _formatTime(self, time):
        time = int(time / 1000)
        s = time % 60
        m = int(time / 60)
        h = int(time / 3600)
        return f"{h}:{m:02}:{s:02}"

    @Slot(QUrl)
    def open(self, file_path: QUrl):
        logger.info(f"open video file: [{file_path}]")
        self.file_path = file_path
        try:
            self.video_widget.stop()
            # FIX: WTF .... https://stackoverflow.com/questions/77219901/can-not-change-media-using-setsource-in-pyside6
            QThread.msleep(200)
            self.video_widget.setVideo(file_path)
            self.video_widget.play()
        except Exception as error:
            logger.error(f"open video error: [{error}]")

    def _onAddSubtitle(self):
        logger.info("add subtitle")
        diaglog = QFileDialog(
            self, "Choose a video subtitle file", self.file_path.toLocalFile()
        )
        diaglog.setFileMode(QFileDialog.FileMode.ExistingFile)
        diaglog.setAcceptMode(QFileDialog.AcceptOpen)

        diaglog.setNameFilter("SRT Files (*.srt)")
        if diaglog.exec() == QDialog.Accepted:
            self.subtitle_path = diaglog.selectedUrls()[0]
            logger.info(f"subtitle file: [{self.subtitle_path}]")

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        menu = RoundMenu(parent=self)

        menu.addAction(
            QAction(
                FIF.CHAT.icon(),
                self.tr("Add Subtitle"),
                self,
                triggered=self._onAddSubtitle,
            )
        )

        menu.exec(self.mapToGlobal(event))
