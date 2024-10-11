from ChatWidget_ui import Ui_ChatWidget
from LLM.ChatRAGChain import ChatRAGChain
from LLM.ChatWithCustomHistoryChain import ChatLLMWithCustomHistory
from LLM.ChatWorkerThread import ChatWorkThread
from MessageBox import CMessageBox
from ModuleLogger import logger
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon as FIF
import asyncio


class ChatWidget(QWidget, Ui_ChatWidget):
    """
    A widget for handling chat interactions, including sending messages and checking input.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.messages_list.setAlignment(Qt.AlignTop)
        self.chat_scroll_area.setStyleSheet(
            "QScrollArea{background: transparent; border: none}"
        )
        # Must also set transparent background style for the internal view
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
        """
        Sets the RAG data reader.

        Args:
            reader: The data reader to be used by the chat chain.
        """
        self.chat_chain = None
        self.reader = reader

    def connectSignal(self):
        """Connects the signals to their respective slots."""
        self.user_send_button.clicked.connect(
            lambda: asyncio.ensure_future(self.sendMessage())
        )
        self.user_check_button.clicked.connect(
            lambda: asyncio.ensure_future(self.checkInput())
        )

    async def initChatChain(self):
        """Initializes the chat chain if it is not already initialized."""
        if self.chat_chain is None:
            self.chat_chain = ChatRAGChain(self.reader)
            await self.chat_chain.createChatChain()

    def initCheckChain(self):
        """Initializes the check chain if it is not already initialized."""
        if self.check_chain is None:
            self.check_chain = ChatLLMWithCustomHistory()

    async def sendMessage(self):
        """Handles the sending of a message."""
        if self.need_update_label is not None:
            return
        await self.initChatChain()
        # try:
        # except Exception as e:
        #     logger.error(e)
        #     return
        self.user_send_button.setEnabled(False)

        message_text = self.user_text_edit.toPlainText()
        self.user_text_edit.setText("")

        if message_text:
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
    async def checkInput(self):
        """Handles the checking of input."""
        if self.need_update_label is not None:
            return
        try:
            await self.initChatChain()
            self.initCheckChain()
        except Exception as e:
            logger.error(e)
            return
        self.user_check_button.setEnabled(False)
        message_text = self.user_text_edit.toPlainText()
        if message_text:
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
        """Slot called when the worker thread starts."""
        self.user_send_button.setEnabled(False)
        self.user_check_button.setEnabled(False)
        self.messages_list.update()

    @Slot()
    def workerThreadFinish(self):
        """Slot called when the worker thread finishes."""
        self.user_send_button.setEnabled(True)
        self.user_check_button.setEnabled(True)
        self.messages_list.update()
        self.need_update_label = None

    @Slot(str)
    def updateLabel(self, message):
        """
        Updates the label with the given message.

        Args:
            message (str): The message to update the label with.
        """
        if self.need_update_label is not None:
            self.need_update_label.setMessageText(
                self.need_update_label.getMessageText() + message
            )
