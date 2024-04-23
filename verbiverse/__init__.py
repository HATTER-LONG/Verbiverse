import asyncio
import sys

import PySide6.QtAsyncio as QtAsyncio
from ChatLLM import ChatChain
from MainWindow import Ui_MainWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("聊天界面")

        self.messages_list_widget = QWidget()
        self.messages_list = QVBoxLayout(
            self.messages_list_widget
        )  # Change to QVBoxLayout
        self.messages_list.setAlignment(Qt.AlignTop)

        self.messages_list_widget.setContentsMargins(0, 0, 0, 0)

        self.chatScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vscrollbar = self.chatScrollArea.verticalScrollBar()
        self.vscrollbar.rangeChanged.connect(self.scrollToBottomIfNeeded)
        self.adding = False

        self.chatScrollArea.setWidgetResizable(True)
        self.chatScrollArea.setWidget(self.messages_list_widget)

        self.userTextEdit.setPlaceholderText("输入消息")
        self.userSendButton.clicked.connect(
            lambda: asyncio.ensure_future(self.send_Message())
        )
        self.chat_chain = ChatChain()

    def scrollToBottomIfNeeded(self, minimum, maximum):
        if self.adding:
            self.vscrollbar.setValue(maximum)
            self.adding = False

    async def send_Message(self):
        self.userSendButton.setEnabled(False)
        message_text = self.userTextEdit.toPlainText()
        if message_text:
            message_label = QLabel(f"You: {message_text}")
            message_label.setWordWrap(True)
            self.messages_list.addWidget(message_label)  # Add to QVBoxLayout
            self.userTextEdit.setText("")

            content = self.chat_chain.stream(message_text)

            reply_text = ""
            reply_label = QLabel(f"Robot: {reply_text}")
            reply_label.setWordWrap(True)
            self.messages_list.addWidget(reply_label)  # Add to QVBoxLayout
            self.adding = True
            for chunk in content:
                print(reply_label.text() + chunk.content)
                reply_label.setText(reply_label.text() + chunk.content)
                QApplication.processEvents()
        self.userSendButton.setEnabled(True)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

QtAsyncio.run()
