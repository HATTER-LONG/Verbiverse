from Functions.Config import cfg
from langchain_openai import ChatOpenAI, OpenAI
from ModuleLogger import logger
from qfluentwidgets import qconfig


def getOpenAIChatModel() -> ChatOpenAI:
    api_key = qconfig.get(cfg.user_key)
    api_url = qconfig.get(cfg.provider_url)
    model = qconfig.get(cfg.model_name)

    logger.info("ChatGPT model: %s", model)
    logger.info("ChatGPT API key: %s", api_key)
    logger.info("ChatGPT API url: %s", api_url)

    return ChatOpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )


def getOpenAILLMModel() -> OpenAI:
    api_key = qconfig.get(cfg.user_key)
    api_url = qconfig.get(cfg.provider_url)
    model = qconfig.get(cfg.model_name)

    return OpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )
