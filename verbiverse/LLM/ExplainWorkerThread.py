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
    """Worker thread for ExplainChain"""
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
        """
        Check if the given `selected_text` is a sentence by counting the number of words in it.

        Parameters:
            selected_text (str): The text to be checked.

        Returns:
            bool: True if the `selected_text` has more than one word, False otherwise.
        """
        words = re.findall(r"\b\w+\b", selected_text)

        if len(words) > 1:
            return True
        else:
            return False

    def createExplainChain(self, selected_text: str, all_text: str) -> None:
        """
        Creates an explain chain for the given selected text and all text.

        Args:
            selected_text (str): The selected text to be explained.
            all_text (str): The entire text context.

        Returns:
            None: This function does not return anything.

        Raises:
            Exception: If there is an error getting the chat model.

        Description:
            This function initializes the explain chain for the given selected text and all text. It first tries to get the chat model using the `getChatModelByCfg` function. If there is an error, it logs the error and returns. It then sets the target language and answer language based on the type of the explain. It creates a prompt template using the `getExplainPrompt` function and combines it with the chat model to create the explain chain. It creates a message dictionary with the selected text, all text, target language, and answer language. Finally, it logs the explain request message.
        """
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
        """
        A function that stops the worker thread by setting the quit flag to True.
        """
        self.quit = True

    def run(self):
        """
        Runs the explain worker thread.

        This function checks if the explain chain is set. If not, it logs an error message and returns.
        If the explain chain is set, it tries to stream the message or invoke it depending on the value of the `stream` attribute.
        If streaming is enabled, it iterates over the content chunks and emits each chunk's content using the `messageCallBackSignal` signal.
        If streaming is disabled, it invokes the chain with the message and emits the content using the `messageCallBackSignal` signal.
        If an exception occurs during the process, it logs an error message with the exception details and emits an error signal with a formatted error message.

        Parameters:
            None

        Returns:
            None
        """
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
