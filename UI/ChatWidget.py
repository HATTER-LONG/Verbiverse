from ChatWidget_ui import Ui_ChatWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget


class ChatWidget(QWidget, Ui_ChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.messages_list_widget = QWidget(self.chat_scroll_area)
        self.messages_list = QVBoxLayout(self.messages_list_widget)
        self.messages_list.setAlignment(Qt.AlignTop)
        self.messages_list_widget.setContentsMargins(0, 0, 0, 0)

        # Link messages list to scroll arean
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setWidget(self.messages_list_widget)

        # self.chat_scroll_area.setStyleSheet(
        #     "QScrollArea{background: transparent; border: none}"
        # )

        # # 必须给内部的视图也加上透明背景样式
        # self.messages_list_widget.setStyleSheet("QWidget{background: transparent}")
