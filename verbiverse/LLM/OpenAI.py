from Functions.Config import cfg
from Functions.ErrorString import error_string
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from ModuleLogger import logger
from qfluentwidgets import qconfig


def __getConfig() -> (str, str, str):
    """
    Retrieves the API key, API URL, and model name required for OpenAI interaction.
    Raises exceptions if any of the essential configurations are missing.

    Returns:
        Tuple containing the API key, API URL, and model name.
    """
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
    """
    Retrieves an instance of the ChatOpenAI class with the OpenAI API key, URL, and model name
    obtained from the getConfig() function.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class with the specified API key, URL, model name,
        and temperature set to 0.7.
    """
    api_key, api_url, model = __getConfig()

    return ChatOpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )


def getOpenAIEmbedding() -> OpenAIEmbeddings:
    api_key, api_url, model = __getConfig()
    return OpenAIEmbeddings(
        model="mixedbread-ai/mxbai-embed-large-v1",
        openai_api_key="lm-studio",
        openai_api_base=api_url,
        check_embedding_ctx_length=False,
    )


def getOpenAILLMModel() -> OpenAI:
    """
    Retrieves an instance of the OpenAI class with the OpenAI API key, URL, and model name
    obtained from the getConfig() function.

    Returns:
        OpenAI: An instance of the OpenAI class with the specified model name,
        API key, API URL, and temperature set to 0.7.
    """
    api_key, api_url, model = __getConfig()

    return OpenAI(
        model_name=model,
        openai_api_key=api_key,
        openai_api_base=api_url,
        temperature=0.7,
    )
