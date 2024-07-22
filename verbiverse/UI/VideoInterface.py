from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import QUrl, Slot
from PySide6.QtWidgets import QWidget
from VideoInterface_ui import Ui_VideoInterface


class VideoInterface(QWidget, Ui_VideoInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        signalBus.open_video_signal.connect(self.open)

    @Slot(QUrl)
    def open(self, file_path: QUrl):
        logger.info(f"open video file: [{file_path}]")
        try:
            self.video_widget.setVideo(file_path)
            self.video_widget.play()
        except Exception as error:
            logger.error(f"open video error: [{error}]")
