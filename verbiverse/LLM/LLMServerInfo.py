from Functions.Config import cfg
from ModuleLogger import logger
from OpenAI import getOpenAIChatModel
from PySide6.QtCore import QFile, QIODevice
from qfluentwidgets import qconfig
from TongYiQWen import getTongYiChatModel


# Helper function to load a resource from the specified path with error handling
def __getPromptResource(prompt_name: str) -> str:
    """
    Loads a text file from the resources directory, given its name.

    Args:
        prompt_name (str): The name of the text file without the file extension.

    Returns:
        str: Content of the file as a string.

    Raises:
        FileNotFoundError: If the file cannot be opened.
    """
    content = ""
    file = QFile(prompt_name)
    if file.open(QIODevice.ReadOnly | QIODevice.Text):
        content = str(file.readAll(), encoding="utf-8")
        file.close()
    else:
        raise FileNotFoundError(f"Error opening file: {file.errorString()}")
    return content


# Retrieves the chat prompt text from a resource
def getChatPrompt() -> str:
    """
    Loads the chat prompt text from the resources directory.

    :return: The chat prompt as a string.
    """
    return __getPromptResource(":/prompt/chat_prompt.txt")


# Retrieves the check prompt text from a resource
def getCheckPrompt() -> str:
    """
    Loads the check prompt text from the resources directory.

    :return: The check prompt as a string.
    """
    return __getPromptResource(":/prompt/check_CN.txt")


# Retrieves the translate by English prompt text from a resource
def getTranslateByENPrompt() -> str:
    """
    Loads the translation prompt for English from the resources directory.

    :return: The translation prompt for English as a string.
    """
    return __getPromptResource(":/prompt/translate_EN.txt")


# Retrieves the translate by Chinese prompt text from a resource
def getTranslateByCNPrompt() -> str:
    """
    Loads the translation prompt for Chinese from the resources directory.

    :return: The translation prompt for Chinese as a string.
    """
    return __getPromptResource(":/prompt/translate_CN.txt")


def getExplainByENPrompt() -> str:
    return __getPromptResource(":/prompt/explain_EN.txt")


def getChatModelByCfg():
    chat = None
    provider = qconfig.get(cfg.provider)
    if provider == "openai":
        chat = getOpenAIChatModel()
    elif provider == "tongyi":
        chat = getTongYiChatModel()
    else:
        raise Exception(f"Not supported {provider} for now")
    return chat
