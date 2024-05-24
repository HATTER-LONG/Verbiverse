from ChatWidget_ui import Ui_ChatWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget


class ChatWidget(QWidget, Ui_ChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.chat_scroll_area.setStyleSheet(
            "QScrollArea{background: transparent; border: none}"
        )

        # 必须给内部的视图也加上透明背景样式
        self.scroll_area_widget.setStyleSheet("QWidget{background: transparent}")
