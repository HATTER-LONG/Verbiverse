from PySide6.QtWidgets import QWidget
from ReadAndChatWidget_ui import Ui_ReadAndChatWidget


class ReadAndChatWidget(QWidget, Ui_ReadAndChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
