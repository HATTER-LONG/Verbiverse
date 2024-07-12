import json
import os

from CFileListWidget_ui import Ui_CFileListWidget
from Functions.Config import CONFIG_PATH
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtWidgets import QListWidgetItem, QWidget
from qfluentwidgets import FluentIcon


class CFileListWidget(QWidget, Ui_CFileListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loadConfigFile()
        self.refreshList()
        self.filelist_clear.setIcon(FluentIcon.DELETE)
        self.filelist_widget.doubleClicked.connect(self.doubleClicked)
        self.filelist_clear.clicked.connect(self.clear)
        signalBus.open_localfile_signal.connect(self.addFile)

    def updateConfig(self):
        if os.path.exists(CONFIG_PATH + "historyfilelist.json"):
            with open(CONFIG_PATH + "historyfilelist.json", "w", encoding="utf-8") as f:
                # f.seek(0)
                # f.truncate()
                json.dump(self.file_list, f)

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

    @Slot(QUrl)
    def addFile(self, file_url: QUrl):
        file_path = file_url.toLocalFile()
        self.updateFileList(file_path)
        self.refreshList()
        self.updateConfig()

    def refreshList(self):
        self.filelist_widget.clear()
        for file_item in reversed(self.file_list):
            file_name = os.path.basename(file_item)
            item = QListWidgetItem(file_name)
            item.setIcon(FluentIcon.DOCUMENT.icon())
            item.setData(Qt.UserRole, file_item)
            self.filelist_widget.addItem(item)

    def updateFileList(self, file_path: str):
        if file_path in self.file_list:
            self.file_list.remove(file_path)
        if len(self.file_list) == 10:
            self.file_list.pop(0)
        self.file_list.append(file_path)

    @Slot()
    def clear(self):
        self.file_list = []
        self.refreshList()
        self.updateConfig()

    @Slot(QListWidgetItem)
    def doubleClicked(self, item: QListWidgetItem):
        file_path = item.data(Qt.UserRole)
        print(file_path)
        signalBus.open_localfile_signal.emit(QUrl.fromLocalFile(file_path))
