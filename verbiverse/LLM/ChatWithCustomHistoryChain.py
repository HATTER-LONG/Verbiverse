from Functions.SignalBus import signalBus
from langchain_core.prompts import PromptTemplate
from LLMServerInfo import getChatModelByCfg, getCheckPrompt
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
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.content = getCheckPrompt()

        self.prompt = PromptTemplate.from_template(self.content)

        self.chain = self.prompt | self.chat
        self.chat_history_for_chain = None

    def setChatHistoryForChain(self, chat_message_history: str):
        """
        Set the chat history for the langchain chat model.

        :param chat_message_history: A string representing the chat history.
        """
        self.chat_history_for_chain = chat_message_history

    def stream(self, message: str):
        """
        Call the langchain chat model with the given message and chat history.

        :param message: A string representing the message to send to the chat model.
        :return: A generator yielding the responses from the chat model.
        """
        msg = {"data": message, "history": self.chat_history_for_chain}
        return self.chain.stream(msg)
