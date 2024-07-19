from Functions.Config import cfg
from Functions.LanguageType import ExplainLanguage
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from OpenAI import getOpenAIChatModel, getOpenAIEmbedding
from PySide6.QtCore import QFile, QIODevice
from qfluentwidgets import qconfig
from TongYiQWen import getTongYiChatModel, getDashScopeEmbedding


# Helper function to load a resource from the specified path with error handling
def __getPromptResource(prompt_name: str) -> str:
    """
    Retrieves the content of a resource file specified by `prompt_name`.

    Args:
        prompt_name (str): The path to the resource file.

    Returns:
        str: The content of the resource file.

    Raises:
        FileNotFoundError: If the resource file cannot be opened.

    This function opens a resource file specified by `prompt_name` and reads its content. It uses the `QFile` class from the PySide6 library to open the file in read-only mode with text encoding. If the file is successfully opened, the content is read and returned. If the file cannot be opened, a `FileNotFoundError` is raised with an error message indicating the reason for the failure.

    Example:
        >>> __getPromptResource("path/to/resource.txt")
        "This is the content of the resource file."
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
    return __getPromptResource(":/prompt/chat_prompt.txt")


# Retrieves the check prompt text from a resource
def getCheckPrompt() -> str:
    language = qconfig.get(cfg.mother_tongue)

    logger.info(f"check prompt for {language} -> :/prompt/check_{language}.txt")
    try:
        return __getPromptResource(f":/prompt/check_{language}.txt")
    except Exception:
        logger.warning(
            f"Not found explain prompt for {language} -> :/prompt/explain_{language}.txt. Used default prompt"
        )
        return __getPromptResource(":/prompt/check_prompt.txt")


# Retrieves the translate by English prompt text from a resource


def __getExplainPromptByLanguage(prompt: str, default_prompt: str) -> str:
    """
    Retrieves the explain prompt for a specific language based on the provided prompt name.

    Args:
        prompt (str): The prompt name to retrieve.
        default_prompt (str): The default prompt to use if the specified prompt is not found.

    Returns:
        str: The explain prompt text based on the provided prompt or the default prompt if not found.
    """
    try:
        return __getPromptResource(prompt)
    except Exception:
        logger.warning(
            f"Not found explain prompt for {prompt}. Used default {default_prompt}"
        )
        return __getPromptResource(default_prompt)


def getExplainPrompt(
    answer_language: ExplainLanguage = None, is_sentence: bool = False
) -> str:
    """
    Retrieves the explain prompt based on the specified answer language and sentence type.

    Args:
        answer_language (ExplainLanguage, optional): The language to use for the explain prompt. Defaults to None.
        is_sentence (bool, optional): Flag indicating whether the prompt is for a sentence. Defaults to False.

    Returns:
        str: The explain prompt.

    Raises:
        None

    Examples:
        >>> getExplainPrompt(answer_language=ExplainLanguage.TARGET_LANGUAGE)
        "/prompt/explain_en.txt"
    """
    explain_prefix = "explain"
    explain_default_prompt = ":/prompt/explain_prompt.txt"
    if is_sentence:
        explain_prefix = "explain_sentence"
        explain_default_prompt = ":/prompt/explain_sentence_prompt.txt"

    if answer_language == ExplainLanguage.TARGET_LANGUAGE:
        language = qconfig.get(cfg.target_language)
        prompt_name = f":/prompt/{explain_prefix}_{language}.txt"
        logger.info(f"explain prompt for target {language} -> {prompt_name}")
        return __getExplainPromptByLanguage(
            prompt_name, default_prompt=explain_default_prompt
        )
    elif answer_language == ExplainLanguage.MOTHER_TONGUE:
        language = qconfig.get(cfg.mother_tongue)
        prompt_name = f":/prompt/{explain_prefix}_{language}.txt"
        logger.info(f"explain prompt for target {language} -> {prompt_name}")
        return __getExplainPromptByLanguage(
            prompt_name, default_prompt=explain_default_prompt
        )
    else:
        return __getPromptResource(":/prompt/explain_prompt.txt")


def getChatModelByCfg():
    """
    Retrieves a chat model based on the configuration.

    This function retrieves a chat model based on the provider specified in the configuration. The provider can be either "openai" or "tongyi". If the provider is "openai", it calls the `getOpenAIChatModel` function to get the chat model. If the provider is "tongyi", it calls the `getTongYiChatModel` function to get the chat model. If the provider is neither "openai" nor "tongyi", it raises an exception.

    Returns:
        The chat model corresponding to the provider specified in the configuration.

    Raises:
        Exception: If the provider specified in the configuration is not supported.
    """
    chat = None
    provider = qconfig.get(cfg.provider)
    try:
        if provider == "openai":
            chat = getOpenAIChatModel()
        elif provider == "tongyi":
            chat = getTongYiChatModel()
        else:
            raise Exception(f"Not supported {provider} for now")
    except Exception as e:
        signalBus.error_signal.emit(str(e))
        raise e
    return chat


def getEmbedModelByCfg():
    embed = None
    provider = qconfig.get(cfg.provider)
    try:
        if provider == "openai":
            embed = getOpenAIEmbedding()
        elif provider == "tongyi":
            embed = getDashScopeEmbedding()
        else:
            raise Exception(f"Not supported {provider} for now")
    except Exception as e:
        signalBus.error_signal.emit(str(e))
        raise e
    return embed


def getTargetLanguage():
    """
    Retrieves the target language from the configuration.

    Returns:
        str: The target language in the configuration.
    """
    return qconfig.get(cfg.target_language)


def getMotherTongue():
    """
    Retrieves the mother tongue from the configuration.

    Returns:
        str: The mother tongue specified in the configuration.
    """
    return qconfig.get(cfg.mother_tongue)
