from enum import Enum

from ChatWorkerThread import ChatWorkThread
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from LLMServerInfo import get_api_key, get_api_url, get_model
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from UI import Ui_TranslateInfoWin


class TranslationType(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2


class TranslateInfoWin(QWidget, Ui_TranslateInfoWin):
    def __init__(self, type, selected_text, all_text):
        super(TranslateInfoWin, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(selected_text)
        self.selected_text = selected_text
        self.all_text = all_text
        self.type = type
        if type == TranslationType.MOTHER_TONGUE:
            self.translate_button.setHidden(True)
        else:
            self.translate_button.clicked.connect(self.onTranslateButtonClicked)

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
        self.worker = ChatWorkThread()
        self.worker.setChain(self.chain)
        self.worker.setMessage(msg)
        self.worker.messageCallBackSignal.connect(self.onTranslateResultUpdate)
        self.worker.started.connect(self.workerStart)
        self.worker.finished.connect(self.workerStop)
        self.worker.start()

    @Slot(str)
    def onTranslateResultUpdate(self, res: str):
        self.result.setText(self.result.text() + res)

    @Slot()
    def onTranslateButtonClicked(self):
        if self.worker is not None:
            print("onTranslateButtonClicked not running")
            return

        chat = ChatOpenAI(
            model_name=get_model(),
            openai_api_key=get_api_key(),
            openai_api_base=get_api_url(),
            temperature=0.8,
            max_tokens=4096,
        )
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "你是一个专业的翻译助手，擅长将{source_lang}翻译成{dest_lang}, 对输入的文本进行翻译"
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        self.chain = chat_template | chat

        result = self.result.text()
        splitstr = "\n----------------翻译----------------------\n"
        self.result.setText(result + splitstr)
        # TODO: 多语言兼容
        msg = {"source_lang": "英语", "dest_lang": "中文", "text": result}
        self.worker.setChain(self.chain)
        self.worker.setMessage(msg)
        self.thread.finished.connect(None)
        self.worker.start()

    @Slot()
    def workerStop(self):
        if not self.translate_button.isHidden():
            self.translate_button.setEnabled(True)
        self.worker = None

    @Slot()
    def workerStart(self):
        if not self.translate_button.isHidden():
            self.translate_button.setEnabled(False)
