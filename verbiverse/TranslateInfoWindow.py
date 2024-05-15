import re
from enum import Enum

from ChatWorkerThread import ChatWorkThread
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from LLMServerInfo import (
    getApiKey,
    getApiUrl,
    getModelName,
    getTranslateByCNPrompt,
    getTranslateByENPrompt,
)
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from UI import Ui_TranslateInfoWin
from WordsBookDatabase import WordsBookDatabase


class TranslationType(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2


def isWord(string) -> bool:
    return " " not in string


class TranslateInfoWin(QWidget, Ui_TranslateInfoWin):
    def __init__(self, type, selected_text, all_text):
        super(TranslateInfoWin, self).__init__()
        self.setupUi(self)
        # self.selected_text = selected_text.replace("\n", " ")
        self.selected_text = selected_text
        self.setWindowTitle(selected_text.replace("\n", " "))
        self.all_text = all_text
        self.type = type
        if type == TranslationType.MOTHER_TONGUE:
            self.translate_button.setHidden(True)
        else:
            self.translate_button.clicked.connect(self.onTranslateButtonClicked)

        self.add_database_button.clicked.connect(self.onAddDatabase)
        chat = ChatOpenAI(
            model_name=getModelName(),
            openai_api_key=getApiKey(),
            openai_api_base=getApiUrl(),
            temperature=0.8,
            max_tokens=4096,
        )
        message = ""
        if type == TranslationType.TARGET_LANGUAGE:
            message = getTranslateByENPrompt()
        else:
            message = getTranslateByCNPrompt()
        prompt = PromptTemplate.from_template(message)

        self.chain = prompt | chat

        msg = {"word": self.selected_text, "data": self.all_text}
        print("send msg = ", msg)
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
        self.adjustSize()

    @Slot()
    def onTranslateButtonClicked(self):
        chat = ChatOpenAI(
            model_name=getModelName(),
            openai_api_key=getApiKey(),
            openai_api_base=getApiUrl(),
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
        splitstr = "\n\n----------------翻译----------------------\n\n"
        self.result.setText(result + splitstr)
        # TODO: 多语言兼容
        msg = {"source_lang": "英语", "dest_lang": "中文", "text": result}
        self.worker.setChain(self.chain)
        self.worker.setMessage(msg)
        self.worker.finished.disconnect(self.workerStop)
        self.worker.start()

    @Slot()
    def workerStop(self):
        if not self.translate_button.isHidden():
            self.translate_button.setEnabled(True)

    @Slot()
    def workerStart(self):
        if not self.translate_button.isHidden():
            self.translate_button.setEnabled(False)

    @Slot()
    def onAddDatabase(self):
        db = WordsBookDatabase()
        sentences = re.split(r"[.!?]\s+", self.all_text)
        example = ""
        for sentence in sentences:
            if self.selected_text in sentence:
                example = sentence.strip()
        db.add_word(self.selected_text, example)
