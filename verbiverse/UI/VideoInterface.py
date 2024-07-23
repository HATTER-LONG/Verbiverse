import pysrt
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
        self.parse_button.setIcon(FIF.ROBOT)
        signalBus.open_video_signal.connect(self.open)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)
        self.file_path = None
        self.subtitle_path = None
        self.subtitle = None
        self.last_timestamp = -1
        self.current_subtitle = None
        self.video_widget.playBar.setVolume(80)
        self.video_widget.player.positionChanged.connect(self.postion)

    def postion(self, time):
        if not self.subtitle or (
            time - self.last_timestamp > 0 and time - self.last_timestamp < 500
        ):
            return
        self.last_timestamp = time
        self.current_subtitle = self.subtitle.at(seconds=(time / 1000))
        if len(self.current_subtitle.text) > 0:
            self.subtitle_label.setText(self.current_subtitle.text.replace("\n", " "))
        # current_time_ms = time
        # start_index = max(self.last_subtitle_index, 0)
        # current_subtitle = None
        # for subtitle_index in range(start_index, len(self.subtitle)):
        #     subtitle = self.subtitle[subtitle_index]
        #     logger.debug(f"subtitle: [{subtitle.start.milliseconds}]")

        #     if (
        #         current_time_ms >= subtitle.start.milliseconds
        #         and current_time_ms < subtitle.end.milliseconds
        #     ):
        #         logger.debug(f"current time: [{current_time_ms}]")
        #         self.current_subtitle = subtitle
        #         self.last_subtitle_index = subtitle_index  # Update last index
        #         break

        # if current_subtitle:
        #     self.current_subtitle = current_subtitle
        #     logger.debug(f"current subtitle: [{self.current_subtitle}]")

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
            self.subtitle = pysrt.open(self.subtitle_path.toLocalFile())
            logger.info(f"subtitle count: [{len(self.subtitle)}]")
            logger.debug(f"subtitle: [{self.subtitle[0]}]")
            logger.debug(f"subtitle: [{self.subtitle[0].start}]")

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
