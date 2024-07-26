import json
import os

from CFileListWidget_ui import Ui_CFileListWidget
from Functions.Config import CONFIG_PATH
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import Qt, QTimer, QUrl, Slot
from PySide6.QtWidgets import QListWidgetItem, QWidget
from qfluentwidgets import FluentIcon


class CFileListWidget(QWidget, Ui_CFileListWidget):
    PDF_FILE = 0
    MEDIA_FILE = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateConfig)
        self.loadConfigFile()
        self.refreshList()
        self.filelist_clear.setIcon(FluentIcon.DELETE)
        self.filelist_widget.doubleClicked.connect(self.doubleClicked)
        self.filelist_clear.clicked.connect(self.clear)
        signalBus.open_localfile_signal.connect(self.addFile)
        signalBus.open_video_signal.connect(self.addVideoFile)
        signalBus.update_file_schedule_signal.connect(self.updateSchedule)
        self.need_update = False
        self.timer.start(5000)

    def updateConfig(self):
        if not self.need_update:
            return
        self.need_update = False
        logger.debug("update filelist: %s" % self.file_list)
        if os.path.exists(CONFIG_PATH + "historyfilelist.json"):
            with open(CONFIG_PATH + "historyfilelist.json", "w", encoding="utf-8") as f:
                json.dump(self.file_list, f)
        self.refreshList()

    def loadConfigFile(self):
        if os.path.exists(CONFIG_PATH + "historyfilelist.json"):
            with open(CONFIG_PATH + "historyfilelist.json", "r", encoding="utf-8") as f:
                try:
                    self.file_list = json.load(f)
                except Exception as e:
                    logger.error("load filelist.json error: %s" % e)
                    self.file_list = []
        else:
            self.file_list = []
            if not os.path.exists(CONFIG_PATH):
                os.makedirs(CONFIG_PATH)
            with open(CONFIG_PATH + "historyfilelist.json", "w", encoding="utf-8") as f:
                json.dump(self.file_list, f)

    @Slot(str, int)
    def updateSchedule(self, file_path: str, schedule: int):
        index = self.getIndex(file_path)
        self.file_list[index]["schedule"] = schedule
        # item = self.filelist_widget.item(len(self.file_list) - index - 1)
        # item.setText(f"{os.path.basename(file_path)}  {self._formatTime(schedule)}")
        self.need_update = True

    @Slot(QUrl, int)
    def addFile(self, file_url: QUrl, schedule: int):
        file_path = file_url.toLocalFile()
        self.updateFileList(file_path, self.PDF_FILE, schedule)
        self.refreshList()
        self.need_update = True

    @Slot(QUrl, int)
    def addVideoFile(self, file_url: QUrl, schedule: int):
        file_path = file_url.toLocalFile()
        self.updateFileList(file_path, self.MEDIA_FILE, schedule)
        self.refreshList()
        self.need_update = True

    def refreshList(self):
        self.filelist_widget.clear()
        for file_item in reversed(self.file_list):
            file_name = os.path.basename(file_item["file_path"])

            schedule = file_item["schedule"]
            icon = FluentIcon.DOCUMENT.icon()
            if file_item["file_type"] == self.MEDIA_FILE:
                schedule = self._formatTime(schedule)
                icon = FluentIcon.VIDEO.icon()

            item = QListWidgetItem(f"{file_name}  {schedule}")
            item.setIcon(icon)
            item.setData(Qt.UserRole, file_item)
            self.filelist_widget.addItem(item)

    def _formatTime(self, time: int):
        time = int(time / 1000)
        s = time % 60
        m = int(time / 60)
        h = int(time / 3600)
        return f"{h}:{m:02}:{s:02}"

    def getIndex(self, file_path: str):
        for i, file_item in enumerate(self.file_list):
            if file_item["file_path"] == file_path:
                return i

    def updateFileList(self, file_path: str, file_type: int, schedule: int):
        logger.debug("filelist: %s" % file_path)
        if file_path in [file_item["file_path"] for file_item in self.file_list]:
            del self.file_list[self.getIndex(file_path)]
        if len(self.file_list) == 20:
            self.file_list.pop(0)
        self.file_list.append(
            {"file_path": file_path, "file_type": file_type, "schedule": schedule}
        )
        logger.debug("after update filelist: %s" % self.file_list)

    @Slot()
    def clear(self):
        self.file_list = []
        self.refreshList()
        self.need_update = True

    @Slot(QListWidgetItem)
    def doubleClicked(self, item: QListWidgetItem):
        item = item.data(Qt.UserRole)
        print(item)
        if item["file_type"] == self.PDF_FILE:
            signalBus.open_localfile_signal.emit(
                QUrl.fromLocalFile(item["file_path"]), item["schedule"]
            )
        elif item["file_type"] == self.MEDIA_FILE:
            signalBus.open_video_signal.emit(
                QUrl.fromLocalFile(item["file_path"]), item["schedule"]
            )
