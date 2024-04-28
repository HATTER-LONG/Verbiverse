import sys

from ChatLLM import ChatChain
from MainWindow import Ui_MainWindow
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class WorkThread(QThread):
    messageChanged = Signal(str)  # Declare a signal here using @pyqtSignal()

    def __init__(self, message, chat_chain) -> None:
        super().__init__()
        self.message = message
        self.chat_chain = chat_chain

    def run(self):
        content = self.chat_chain.stream(self.message)
        for chunk in content:
            self.messageChanged.emit(chunk.content)


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

        self.chatScrollArea.setWidgetResizable(True)
        self.chatScrollArea.setWidget(self.messages_list_widget)

        self.userTextEdit.setPlaceholderText("输入消息")
        self.userSendButton.clicked.connect(self.send_Message)
        self.chat_chain = ChatChain()
        self.worker = None
        self.need_update_label = None

    def updateFinish(self):
        self.userSendButton.setEnabled(True)
        self.worker = None
        self.messages_list.update()
        self.vscrollbar.setValue(self.vscrollbar.maximum())

    def updateStart(self):
        self.messages_list.update()
        QApplication.processEvents()
        self.vscrollbar.setValue(self.vscrollbar.maximum())

    def send_Message(self):
        self.userSendButton.setEnabled(False)
        message_text = self.userTextEdit.toPlainText()
        if message_text:
            message_label = QLabel(f"You: {message_text}")
            message_label.setWordWrap(True)
            self.messages_list.addWidget(message_label)  # Add to QVBoxLayout
            self.userTextEdit.setText("")

            reply_text = ""
            self.need_update_label = QLabel(f"Robot: {reply_text}")
            self.need_update_label.setWordWrap(True)
            self.messages_list.addWidget(self.need_update_label)  # Add to QVBoxLayout

            self.worker = WorkThread(message_text, self.chat_chain)
            self.worker.finished.connect(self.updateFinish)
            self.worker.started.connect(self.updateStart)
            self.worker.messageChanged.connect(self.update_label)
            self.worker.start()
        self.vscrollbar.setValue(self.vscrollbar.maximum())

    def update_label(self, message):
        if self.need_update_label is not None:
            self.need_update_label.setText(self.need_update_label.text() + message)
            self.vscrollbar.setValue(self.vscrollbar.maximum())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
