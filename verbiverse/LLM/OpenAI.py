from Functions.Config import cfg
from langchain_openai import ChatOpenAI, OpenAI
from ModuleLogger import logger
from qfluentwidgets import qconfig


def getOpenAIChatModel() -> ChatOpenAI:
    api_key = qconfig.get(cfg.user_key)
    api_url = qconfig.get(cfg.provider_url)
    model = qconfig.get(cfg.model_name)

    logger.info("OpenAI Chat model: %s", model)
    logger.info("OpenAI Chat API url: %s", api_url)

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

    logger.info("OpenAI LLM model: %s", model)
    logger.info("OpenAI LLM API url: %s", api_url)

    return OpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )
