from Functions.Config import cfg
from Functions.ErrorString import error_string
from langchain_openai import ChatOpenAI, OpenAI
from ModuleLogger import logger
from qfluentwidgets import qconfig


def getConfig() -> (str, str, str):
    api_key = qconfig.get(cfg.user_key)
    api_url = qconfig.get(cfg.provider_url)
    model = qconfig.get(cfg.model_name)

    logger.info("OpenAI model: %s", model)
    logger.info("OpenAI API url: %s", api_url)
    if model == "":
        raise Exception(error_string.NO_VALID_LLM_NAME)
    if api_key == "":
        raise Exception(error_string.NO_VALID_LLM_API)
    if api_url == "":
        raise Exception(error_string.NO_VALID_LLM_URL)

    return api_key, api_url, model


def getOpenAIChatModel() -> ChatOpenAI:
    api_key, api_url, model = getConfig()

    return ChatOpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )


def getOpenAILLMModel() -> OpenAI:
    api_key, api_url, model = getConfig()

    return OpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )
