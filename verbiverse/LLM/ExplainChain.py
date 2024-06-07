from Functions.Config import cfg
from langchain_core.prompts import (
    PromptTemplate,
)
from LLMServerInfo import getChatModelByCfg, getExplainByENPrompt
from ModuleLogger import logger
from qfluentwidgets import qconfig


class ExplainChain:
    def __init__(self):
        self.chain = None
        self.createExplainChain()

    def createExplainChain(self) -> None:
        self.chain_with_trimming = None
        provider = qconfig.get(cfg.provider)
        logger.info("explain provider is: %s", provider)
        logger.info("explain model is: %s", qconfig.get(cfg.model_name))
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.prompt = PromptTemplate.from_template(getExplainByENPrompt())

        self.chain = self.prompt | self.chat
