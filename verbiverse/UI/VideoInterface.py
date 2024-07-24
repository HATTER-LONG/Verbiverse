import os
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
            if len(self.current_subtitle.text) < 100:
                self.subtitle_label.setText(
                    self.current_subtitle.text.replace("\n", " ")
                )
            else:
                self.subtitle_label.setText(self.current_subtitle.text)

    def _formatTime(self, time):
        time = int(time / 1000)
        s = time % 60
        m = int(time / 60)
        h = int(time / 3600)
        return f"{h}:{m:02}:{s:02}"

    @Slot(QUrl)
    def open(self, file_path: QUrl):
        logger.info(f"open video file: [{file_path}]")
        self.file_path = file_path.toLocalFile()
        try:
            self.video_widget.stop()
            # FIX: WTF .... https://stackoverflow.com/questions/77219901/can-not-change-media-using-setsource-in-pyside6
            QThread.msleep(200)
            self.video_widget.setVideo(file_path)
            self.video_widget.play()
            self.findSubtitle()
        except Exception as error:
            logger.error(f"open video error: [{error}]")

    def findSubtitle(self):
        file_dir = os.path.dirname(self.file_path)
        file_name = os.path.basename(self.file_path)
        srt_name = os.path.splitext(file_name)[0] + ".srt"
        srt_path = os.path.join(file_dir, srt_name)

        if os.path.exists(srt_path):
            logger.info(f"subtitle file: [{srt_path}]")
            self.subtitle = pysrt.open(srt_path)
            signalBus.info_signal.emit("Auto load subtitle file: " + srt_path)

    def _onAddSubtitle(self):
        logger.info("add subtitle")
        diaglog = QFileDialog(self, "Choose a video subtitle file", self.file_path)
        diaglog.setFileMode(QFileDialog.FileMode.ExistingFile)
        diaglog.setAcceptMode(QFileDialog.AcceptOpen)

        diaglog.setNameFilter("SRT Files (*.srt)")
        if diaglog.exec() == QDialog.Accepted:
            self.subtitle_path = diaglog.selectedUrls()[0]
            logger.info(f"subtitle file: [{self.subtitle_path}]")
            self.subtitle = pysrt.open(self.subtitle_path.toLocalFile())

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
