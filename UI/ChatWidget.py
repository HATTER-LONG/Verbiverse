from ChatWidget_ui import Ui_ChatWidget
from PySide6.QtWidgets import QWidget


class ChatWidget(QWidget, Ui_ChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
