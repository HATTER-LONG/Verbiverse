from enum import Enum

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QThread, Signal, Slot
from UI import Ui_TranslateInfoWin


class TranslationType(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

api_key = "lm-studio"
api_url = "http://localhost:1234/v1"

model = "Qwen/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q5_k_m.gguf"


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
            model_name=model,
            openai_api_key=api_key,
            openai_api_base=api_url,
            temperature=0.7,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a language expert who can analyze and parse given sentences.",
                ),
                (
                    "human",
                    "The term {selected} originates from {input}. Provide a concise English definition and an example sentence.",
                ),
            ]
        )

        self.chain = prompt | chat

        msg = {"selected": self.selected_text, "input": self.all_text}
        self.thread = WorkThread(msg, self.chain)
        self.thread.messageChanged.connect(self.onTranslateResultUpdate)
        self.thread.start()

    @Slot(str)
    def onTranslateResultUpdate(self, res: str):
        self.result.setText(self.result.text() + res)
