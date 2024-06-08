from Functions.Config import cfg
from Functions.LanguageType import ExplainLanguage
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


def __getExplainPromptByLanguage(language: str) -> str:
    try:
        return __getPromptResource(f":/prompt/explain_{language}.txt")
    except Exception:
        logger.warning(
            f"Not found explain prompt for {language} -> :/prompt/explain_{language}.txt. Used default prompt"
        )
        return __getPromptResource(":/prompt/explain_prompt.txt")


def getExplainPrompt(answer_language: ExplainLanguage = None) -> str:
    if answer_language == ExplainLanguage.TARGET_LANGUAGE:
        language = qconfig.get(cfg.target_language)
        logger.info(
            f"explain prompt for target {language} -> :/prompt/explain_{language}.txt"
        )
        return __getExplainPromptByLanguage(language)
    elif answer_language == ExplainLanguage.MOTHER_TONGUE:
        language = qconfig.get(cfg.mother_tongue)
        logger.info(
            f"explain prompt for mother tongue {language} -> :/prompt/explain_{language}.txt"
        )
        return __getExplainPromptByLanguage(language)
    else:
        return __getPromptResource(":/prompt/explain_prompt.txt")


def getExplainByENPrompt() -> str:
    return __getPromptResource(":/prompt/explain_EN.txt")


def getExplainByCNPrompt() -> str:
    return __getPromptResource(":/prompt/explain_CN.txt")


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


def getTargetLanguage():
    return qconfig.get(cfg.target_language)


def getMotherTongue():
    return qconfig.get(cfg.mother_tongue)
