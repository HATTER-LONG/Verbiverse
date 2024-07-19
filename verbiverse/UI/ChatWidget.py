from ChatWidget_ui import Ui_ChatWidget
from LLM.ChatRAGChain import ChatRAGChain
from LLM.ChatWithCustomHistoryChain import ChatLLMWithCustomHistory
from LLM.ChatWorkerThread import ChatWorkThread
from MessageBox import CMessageBox
from ModuleLogger import logger
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon as FIF


class ChatWidget(QWidget, Ui_ChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.messages_list.setAlignment(Qt.AlignTop)
        self.chat_scroll_area.setStyleSheet(
            "QScrollArea{background: transparent; border: none}"
        )
        # 必须给内部的视图也加上透明背景样式
        self.scroll_area_widget.setStyleSheet("QWidget{background: transparent}")

        self.chat_chain = None
        self.check_chain = None
        self.chat_worker = ChatWorkThread()
        self.chat_worker.finished.connect(self.workerThreadFinish)
        self.chat_worker.started.connect(self.workerThreadStart)
        self.chat_worker.messageCallBackSignal.connect(self.updateLabel)

        self.need_update_label = None
        self.user_send_button.setIcon(FIF.SEND)
        self.user_check_button.setIcon(FIF.EDIT)
        self.connectSignal()

    def setRAGData(self, reader):
        self.chat_chain = None
        self.reader = reader

    def connectSignal(self):
        self.user_send_button.clicked.connect(self.sendMessage)
        self.user_check_button.clicked.connect(self.checkInput)

    def initChatChain(self):
        if self.chat_chain is None:
            self.chat_chain = ChatRAGChain(self.reader)

    def initCheckChain(self):
        if self.check_chain is None:
            self.check_chain = ChatLLMWithCustomHistory()

    @Slot()
    def sendMessage(self):
        if self.need_update_label is not None:
            return
        self.user_send_button.setEnabled(False)

        message_text = self.user_text_edit.toPlainText()
        self.user_text_edit.setText("")

        if message_text:
            self.initChatChain()
            message_label1 = CMessageBox(":/images/human_nobg.png", "User", self)
            message_label1.setMessageText(message_text)
            self.messages_list.addWidget(message_label1)

            self.need_update_label = CMessageBox(
                ":/images/robot_nobg.png", "Robot", self
            )
            self.messages_list.addWidget(self.need_update_label)

            self.chat_worker.setChain(self.chat_chain)
            self.chat_worker.setMessage(message_text)
            self.chat_worker.start()

    @Slot()
    def checkInput(self):
        if self.need_update_label is not None:
            return
        self.user_check_button.setEnabled(False)
        message_text = self.user_text_edit.toPlainText()
        if message_text:
            self.initChatChain()
            self.initCheckChain()
            self.need_update_label = CMessageBox(
                ":/images/github_rebot.png", "Robot Checker", self
            )
            self.messages_list.addWidget(self.need_update_label)
            self.check_chain.setChatHistoryForChain(
                self.chat_chain.demo_ephemeral_chat_history_for_chain
            )
            logger.info(self.chat_chain.demo_ephemeral_chat_history_for_chain)
            self.chat_worker.setChain(self.check_chain)

            self.chat_worker.setMessage(message_text)
            self.chat_worker.start()

    @Slot()
    def workerThreadStart(self):
        self.user_send_button.setEnabled(False)
        self.user_check_button.setEnabled(False)
        self.messages_list.update()

    @Slot()
    def workerThreadFinish(self):
        self.user_send_button.setEnabled(True)
        self.user_check_button.setEnabled(True)
        self.messages_list.update()
        self.need_update_label = None

    @Slot(str)
    def updateLabel(self, message):
        if self.need_update_label is not None:
            self.need_update_label.setMessageText(
                self.need_update_label.getMessageText() + message
            )
