import sys

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
        self.userSendButton.clicked.connect(self.send_Message)

    def scrollToBottomIfNeeded(self, minimum, maximum):
        if self.adding:
            self.vscrollbar.setValue(maximum)
            self.adding = False

    def send_Message(self):
        message_text = self.userTextEdit.toPlainText()
        if message_text:
            message_label = QLabel(f"You: {message_text}")
            message_label.setWordWrap(True)
            self.messages_list.addWidget(message_label)  # Add to QVBoxLayout
            self.userTextEdit.setText("")

            # 模拟机器人回复
            reply_text = "你好，我收到你的消息了。"
            reply_label = QLabel(f"Robot: {reply_text}")
            reply_label.setWordWrap(True)
            self.messages_list.addWidget(reply_label)  # Add to QVBoxLayout
            self.adding = True


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
