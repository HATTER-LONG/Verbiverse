import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)

import resources  # noqa: F401
import src  # noqa: F401
from UI import MessageBox, Ui_ChatWidget


class MainWindow(QWidget, Ui_ChatWidget):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont(":/fonts/SEGOEUI.TTF")

        self.setupUi(self)

        self.messages_list_widget = QWidget(self.chat_scroll_area)
        self.messages_list = QVBoxLayout(self.messages_list_widget)
        self.messages_list.setAlignment(Qt.AlignTop)
        self.messages_list_widget.setContentsMargins(0, 0, 0, 0)

        # Link messages list to scroll arean
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setWidget(self.messages_list_widget)

        self.message_label1 = MessageBox(":/title/github.png", "User", self)
        self.message_label1.setMessageText(
            "This is a test message, it's helpful to dev new function avoid input ever time"
        )
        self.messages_list.addWidget(self.message_label1)  # Add to QVBoxLayout
        self.chat_scroll_area.setStyleSheet(
            "QScrollArea{background: transparent; border: none}"
        )

        # 必须给内部的视图也加上透明背景样式
        self.messages_list_widget.setStyleSheet("QWidget{background: transparent}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
