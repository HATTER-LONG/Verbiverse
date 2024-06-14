from Functions.Config import cfg
from Functions.ErrorString import error_string
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from ModuleLogger import logger
from qfluentwidgets import qconfig


def getConfig() -> (str, str):
    api_key = qconfig.get(cfg.user_key)
    model = qconfig.get(cfg.model_name)
    logger.info("TongYi model: %s", model)

    if model == "":
        raise Exception(error_string.NO_VALID_LLM_NAME)
    if api_key == "":
        raise Exception(error_string.NO_VALID_LLM_API)
    return api_key, model


def getTongYiChatModel() -> ChatTongyi:
    api_key, model = getConfig()
    return ChatTongyi(model_name=model, dashscope_api_key=api_key)


def getTongYiLLMModel() -> Tongyi:
    api_key, model = getConfig()
    return Tongyi(
        model_name=model, dashscope_api_key=api_key, top_p=0.8, max_retries=1024
    )
