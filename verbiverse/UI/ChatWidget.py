from ChatWidget_ui import Ui_ChatWidget
from CustomWidgets.ExplainFlyoutView import ExplainFlyoutView
from LLM.ChatChain import ChatChain
from LLM.ChatWithCustomHistoryChain import ChatLLMWithCustomHistory
from LLM.ChatWorkerThread import ChatWorkThread
from MessageBox import CMessageBox
from ModuleLogger import logger
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget
from qfluentwidgets import (
    Flyout,
    FlyoutAnimationType,
)


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

        self.chat_chain = ChatChain()
        self.chat_worker = ChatWorkThread()
        self.chat_worker.finished.connect(self.workerThreadFinish)
        self.chat_worker.started.connect(self.workerThreadStart)
        self.chat_worker.setChain(self.chat_chain)
        self.chat_worker.messageCallBackSignal.connect(self.updateLabel)

        self.check_chain = ChatLLMWithCustomHistory()
        self.check_worker = ChatWorkThread()
        self.check_worker.finished.connect(self.checkFinish)
        self.check_worker.started.connect(self.checkStart)
        self.check_worker.setChain(self.check_chain)
        # self.check_worker.messageCallBackSignal.connect(self.updateFlyout)

        self.need_update_label = None
        self.connectSignal()

    def connectSignal(self):
        self.user_send_button.clicked.connect(self.sendMessage)
        self.user_check_button.clicked.connect(self.checkInput)

    @Slot()
    def sendMessage(self):
        if self.need_update_label is not None:
            return
        self.user_send_button.setEnabled(False)

        message_text = self.user_text_edit.toPlainText()
        self.user_text_edit.setText("")

        if message_text:
            message_label1 = CMessageBox(":/images/github_rebot.png", "User", self)
            message_label1.setMessageText(message_text)
            self.messages_list.addWidget(message_label1)

            self.need_update_label = CMessageBox(
                ":/images/github_rebot.png", "Robot", self
            )
            self.messages_list.addWidget(self.need_update_label)

            self.chat_worker.setMessage(message_text)
            self.chat_worker.start()

    @Slot()
    def workerThreadStart(self):
        self.messages_list.update()

    @Slot()
    def workerThreadFinish(self):
        self.user_send_button.setEnabled(True)
        self.messages_list.update()
        self.need_update_label = None

    @Slot(str)
    def updateLabel(self, message):
        if self.need_update_label is not None:
            self.need_update_label.setMessageText(
                self.need_update_label.getMessageText() + message
            )

    @Slot()
    def checkInput(self):
        message_text = self.user_text_edit.toPlainText()
        if message_text:
            self.check_chain.setChatHistoryForChain(
                self.chat_chain.demo_ephemeral_chat_history_for_chain
            )
            logger.info(self.chat_chain.demo_ephemeral_chat_history_for_chain)

            pos = self.user_check_button.mapToGlobal(self.user_check_button.pos())
            pos.setX(pos.x() - 200)
            self.flyout = Flyout.make(
                ExplainFlyoutView("Check"),
                self.user_check_button,
                self,
                aniType=FlyoutAnimationType.DROP_DOWN,
            )

    @Slot()
    def checkStart(self) -> None:
        pass

    @Slot()
    def checkFinish(self) -> None:
        self.need_update_label = None
