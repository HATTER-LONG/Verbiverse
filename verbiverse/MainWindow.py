import sys

from ChatLLM import ChatChain
from ChatWorkerThread import ChatWorkThread
from MessageBoxWidget import MessageBox
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from UI import Ui_MainWindow


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
        self.need_update_label = None

        self.message_label1 = MessageBox("image", "User")
        self.message_label1.setMessageText(
            "This is a test message, it's helpful to dev new function avoid input ever time"
        )
        self.messages_list.addWidget(self.message_label1)  # Add to QVBoxLayout
        self.worker = ChatWorkThread()
        self.worker.finished.connect(self.updateFinish)
        self.worker.started.connect(self.updateStart)
        self.worker.setChain(self.chat_chain)
        self.worker.messageCallBackSignal.connect(self.update_label)

    @Slot()
    def updateFinish(self):
        self.userSendButton.setEnabled(True)
        self.worker = None
        self.messages_list.update()
        self.vscrollbar.setValue(self.vscrollbar.maximum())
        self.need_update_label = None

    @Slot()
    def updateStart(self):
        self.messages_list.update()
        QApplication.processEvents()
        self.vscrollbar.setValue(self.vscrollbar.maximum())

    @Slot()
    def send_Message(self):
        self.userSendButton.setEnabled(False)
        message_text = self.userTextEdit.toPlainText()
        self.userTextEdit.setText("")
        if message_text:
            message_label = MessageBox("image", "User")
            message_label.setMessageText(message_text)
            self.messages_list.addWidget(message_label)  # Add to QVBoxLayout

            self.need_update_label = MessageBox("image", "Robot")
            self.messages_list.addWidget(self.need_update_label)  # Add to QVBoxLayout

            self.worker.setMessage(message_text)
            self.worker.start()
        self.vscrollbar.setValue(self.vscrollbar.maximum())

    @Slot(str)
    def update_label(self, message):
        if self.need_update_label is not None:
            self.need_update_label.setMessageText(
                self.need_update_label.getMessageText() + message
            )
            self.vscrollbar.setValue(self.vscrollbar.maximum())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
