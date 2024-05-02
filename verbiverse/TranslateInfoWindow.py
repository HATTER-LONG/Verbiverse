from enum import Enum

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from LLMServerInfo import get_api_key, get_api_url, get_model
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QWidget
from UI import Ui_TranslateInfoWin


class TranslationType(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2


# TODO: 冗余代码修正
class WorkThread(QThread):
    # Signal emitted when a new chunk of message content is ready
    messageChanged = Signal(str)

    def __init__(self, message, chat_chain) -> None:
        super().__init__()  # Call the parent constructor
        self.message = message
        self.chat_chain = chat_chain

    @Slot()
    def run(self) -> None:
        content = self.chat_chain.stream(self.message)
        for chunk in content:
            self.messageChanged.emit(chunk.content)


class TranslateInfoWin(QWidget, Ui_TranslateInfoWin):
    def __init__(self, type, selected_text, all_text):
        super(TranslateInfoWin, self).__init__()
        self.setupUi(self)
        self.selected_text = selected_text
        self.all_text = all_text
        self.type = type
        if type == TranslationType.MOTHER_TONGUE:
            self.translate_button.setHidden(True)

        chat = ChatOpenAI(
            model_name=get_model(),
            openai_api_key=get_api_key(),
            openai_api_base=get_api_url(),
            temperature=0.8,
            max_tokens=4096,
        )
        # TODO: 完善提示词加载路径
        message = ""
        if type == TranslationType.TARGET_LANGUAGE:
            with open(
                "/Users/caolei/WorkSpace/Verbiverse/verbiverse/prompt/translate_EN.txt",
                "r",
            ) as file:
                message = file.read()
        else:
            with open(
                "/Users/caolei/WorkSpace/Verbiverse/verbiverse/prompt/translate_CN.txt",
                "r",
            ) as file:
                message = file.read()
        prompt = PromptTemplate.from_template(message)

        self.chain = prompt | chat

        msg = {"word": self.selected_text, "data": self.all_text}
        self.thread = WorkThread(msg, self.chain)
        self.thread.messageChanged.connect(self.onTranslateResultUpdate)
        self.thread.start()

    @Slot(str)
    def onTranslateResultUpdate(self, res: str):
        self.result.setText(self.result.text() + res)
