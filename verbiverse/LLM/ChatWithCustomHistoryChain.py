from Functions.SignalBus import signalBus
from langchain_core.prompts import PromptTemplate
from LLMServerInfo import (
    getChatModelByCfg,
    getCheckPrompt,
    getMotherTongue,
    getTargetLanguage,
)
from ModuleLogger import logger


class ChatLLMWithCustomHistory:
    """
    A class that uses a langchain chat model with a custom chat history.

    The chat history is stored as a string in the `chat_history_for_chain` attribute.
    When calling the `stream` method, this chat history is passed to the langchain chat model
    as a parameter.

    Attributes:
        chain: A langchain chat model.
        chat_history_for_chain: A string representing the chat history.
    """

    def __init__(self):
        self.createChain()
        signalBus.llm_config_change_signal.connect(self.createChain)

    def createChain(self):
        """
        A function that creates a chain by initializing various attributes such as 
        chat, target_language, answer_language, content, prompt, chain, and chat_history_for_chain.
        """
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.target_language = getTargetLanguage()
        self.answer_language = getMotherTongue()

        self.content = getCheckPrompt()

        self.prompt = PromptTemplate.from_template(self.content)

        self.chain = self.prompt | self.chat
        self.chat_history_for_chain = None

    def setChatHistoryForChain(self, chat_message_history: str):
        """
        Set the chat history for the chain.

        Args:
            chat_message_history (str): The chat message history to be set.

        Returns:
            None
        """
        self.chat_history_for_chain = chat_message_history

    def stream(self, message: str):
        """
        Stream a message through the chat model with a custom chat history.

        Args:
            message (str): The message to be streamed.

        Returns:
            The result of streaming the message through the chat model.
        """
        msg = {
            "data": message,
            "history": self.chat_history_for_chain,
            "language": self.target_language,
            "answer_language": self.answer_language,
        }
        return self.chain.stream(msg)
