from Functions.Config import cfg
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from ModuleLogger import logger
from qfluentwidgets import qconfig


def getTongYiChatModel() -> ChatTongyi:
    api_key = qconfig.get(cfg.user_key)
    model = qconfig.get(cfg.model_name)
    # TODO: Check api key valid
    logger.info("TongYi Chat model: %s", model)
    return ChatTongyi(model_name=model, dashscope_api_key=api_key, top_p=0.8)


def getTongYiLLMModel() -> Tongyi:
    api_key = qconfig.get(cfg.user_key)
    model = qconfig.get(cfg.model_name)
    logger.info("TongYi LLM model: %s", model)
    return Tongyi(model_name=model, dashscope_api_key=api_key, top_p=0.8)
