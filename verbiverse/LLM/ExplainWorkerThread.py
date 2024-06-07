from Functions.Config import cfg
from langchain_core.prompts import (
    PromptTemplate,
)
from LLMServerInfo import getChatModelByCfg, getExplainByENPrompt
from ModuleLogger import logger
from PySide6.QtCore import QThread, Signal
from qfluentwidgets import qconfig


class ExplainWorkerThread(QThread):
    messageCallBackSignal = Signal(str)

    def __init__(self, selected_text: str, all_text: str, stream=True):
        super().__init__()
        self.chain = None
        self.stream = stream
        self.msg = {"word": selected_text, "data": all_text}
        logger.info(f"msg is:\n\n {self.msg}\n\n")
        self.createExplainChain()
        self.quit = False

    def createExplainChain(self) -> None:
        self.chain_with_trimming = None
        provider = qconfig.get(cfg.provider)
        logger.debug("explain provider is: %s", provider)
        logger.debug("explain model is: %s", qconfig.get(cfg.model_name))
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.prompt = PromptTemplate.from_template(getExplainByENPrompt())

        self.chain = self.prompt | self.chat

    def stop(self):
        self.quit = True

    def run(self):
        if self.chain is None:
            logger.error("explain chain is not set")
            return
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
