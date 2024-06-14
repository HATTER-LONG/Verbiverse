import re

from Functions.ErrorString import error_string
from Functions.LanguageType import ExplainLanguage
from Functions.SignalBus import signalBus
from langchain_core.prompts import (
    PromptTemplate,
)
from LLMServerInfo import (
    getChatModelByCfg,
    getExplainPrompt,
    getMotherTongue,
    getTargetLanguage,
)
from ModuleLogger import logger
from PySide6.QtCore import QThread, Signal


class ExplainWorkerThread(QThread):
    messageCallBackSignal = Signal(str)

    def __init__(
        self,
        selected_text: str,
        all_text: str,
        language_type: ExplainLanguage,
        stream=True,
    ):
        super().__init__()
        self.chain = None
        self.stream = stream
        self.type = language_type
        self.is_sentence = self.isSentenceString(selected_text)
        self.createExplainChain(selected_text, all_text)
        self.quit = False

    def isSentenceString(self, selected_text: str):
        words = re.findall(r"\b\w+\b", selected_text)

        if len(words) > 1:
            return True
        else:
            return False

    def createExplainChain(self, selected_text: str, all_text: str) -> None:
        self.chain_with_trimming = None
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return
        self.target_language = getTargetLanguage()
        if self.type == ExplainLanguage.TARGET_LANGUAGE:
            self.answer_language = self.target_language
        else:
            self.answer_language = getMotherTongue()

        self.prompt = PromptTemplate.from_template(
            getExplainPrompt(self.type, self.is_sentence)
        )
        self.chain = self.prompt | self.chat

        self.msg = {
            "word": selected_text,
            "data": all_text,
            "language": self.target_language,
            "answer_language": self.answer_language,
        }

        logger.info(f"explain request msg is:\n {self.msg}\n")

    def stop(self):
        self.quit = True

    def run(self):
        if self.chain is None:
            logger.error("explain chain is not set")
            return
        try:
            if self.stream:
                content = self.chain.stream(self.msg)
                for chunk in content:
                    if self.quit:
                        logger.debug("explanation thread quit")
                        return
                    self.messageCallBackSignal.emit(chunk.content)
            else:
                content = self.chain.invoke(self.msg)
                if self.quit:
                    logger.debug("explanation thread quit")
                    return
                self.messageCallBackSignal.emit(content)
        except Exception as e:
            logger.error("explain error: %s", e)
            signalBus.error_signal.emit(error_string.NO_VALID_LLM + str(e))
