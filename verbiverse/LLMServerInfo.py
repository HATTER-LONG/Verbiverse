import resources.resources_rc  # noqa: F401
from PySide6.QtCore import QFile, QIODevice

api_key = "lm-studio"
api_url = "http://localhost:1234/v1"

model = "Qwen/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q5_k_m.gguf"


# Function to retrieve API URL for external communication
def getApiUrl() -> str:
    """
    Returns the API URL used for accessing the service or API.

    :return: The API URL as a string.
    """
    return api_url


# Function to fetch API key for authentication
def getApiKey() -> str:
    """
    Retrieves the API key required for authorization.

    :return: The API key as a string.
    """
    return api_key


# Function to get the name of the model being used
def getModelName() -> str:
    """
    Returns the name of the machine learning model.

    :return: The model name as a string.
    """
    return model


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
    return __getPromptResource(":/prompt/prompt.txt")


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
