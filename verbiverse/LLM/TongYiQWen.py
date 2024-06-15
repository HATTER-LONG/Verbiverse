from Functions.Config import cfg
from Functions.ErrorString import error_string
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from ModuleLogger import logger
from qfluentwidgets import qconfig


def __getConfig() -> (str, str):
    """
    Retrieves the API key and model name required for TongYi interaction.
    
    Returns:
        Tuple containing the API key and model name.
    
    Raises:
        Exception: If the model name or API key is not valid.
    """
    api_key = qconfig.get(cfg.user_key)
    model = qconfig.get(cfg.model_name)
    logger.info("TongYi model: %s", model)

    if model == "":
        raise Exception(error_string.NO_VALID_LLM_NAME)
    if api_key == "":
        raise Exception(error_string.NO_VALID_LLM_API)
    return api_key, model


def getTongYiChatModel() -> ChatTongyi:
    """
    Retrieves the TongYi chat model by calling the `getConfig` function to get the API key and model name.
    
    Returns:
        An instance of the `ChatTongyi` class with the specified model name and API key.
        
    Raises:
        Exception: If the model name or API key is not valid.
    """
    api_key, model = __getConfig()
    return ChatTongyi(model_name=model, dashscope_api_key=api_key)


def getTongYiLLMModel() -> Tongyi:
    """
    Retrieves the TongYi LLM model by calling the `getConfig` function to get the API key and model name.
    
    Returns:
        An instance of the `Tongyi` class with the specified model name, API key, and other parameters.
        
    Raises:
        Exception: If the model name or API key is not valid.
    """
    api_key, model = __getConfig()
    return Tongyi(
        model_name=model, dashscope_api_key=api_key, top_p=0.8, max_retries=1024
    )
