from Functions.SignalBus import signalBus
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from LLMServerInfo import getChatModelByCfg, getChatPrompt, getTargetLanguage
from ModuleLogger import logger


class ChatChain:
    """Chat LLM with message history"""
    def __init__(self):
        self.createChatChain()
        signalBus.llm_config_change_signal.connect(self.createChatChain)

    def createChatChain(self) -> None:
        """
        A function that creates a chat chain by initializing various attributes and objects.
        This function sets up the chat model, target language, chat prompt, and message history for the chain.
        It then creates a chain with message history and applies trimming functionality to it.
        """
        self.chain_with_trimming = None
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.language = getTargetLanguage()
        self.chat_prompt = getChatPrompt()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.chat_prompt,
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        self.chain = self.prompt | self.chat

        self.demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

        self.chain_with_message_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.demo_ephemeral_chat_history_for_chain,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        self.chain_with_trimming = (
            RunnablePassthrough.assign(messages_trimmed=self.trim_messages)
            | self.chain_with_message_history
        )

    def trim_messages(self, jchain_input):
        """
        Trims the messages in the `demo_ephemeral_chat_history_for_chain` attribute to the last 10 messages.
        
        Args:
            jchain_input (Any): The input for the function. Currently not used.
        
        Returns:
            bool: True if the messages were successfully trimmed, False otherwise.
        """
        stored_messages = self.demo_ephemeral_chat_history_for_chain.messages
        if len(stored_messages) <= 10:
            return False

        self.demo_ephemeral_chat_history_for_chain.clear()
        for message in stored_messages[-10:]:
            self.demo_ephemeral_chat_history_for_chain.add_message(message)

        return True

    def invoke(self, message):
        """
        Invokes the chat chain with the given message.

        Args:
            message (str): The message to be sent to the chat chain.

        Returns:
            str or None: The content of the response from the chat chain, or None if the chat chain is not ready.
        """
        if self.chain_with_trimming is None:
            logger.warn("chat chain is not ready")
            return None
        msg = {"input": message}
        return self.chain_with_trimming.invoke(
            msg,
            {"configurable": {"session_id": "unused"}},
        ).content

    def stream(self, message):
        """
        Stream the given message through the chat chain.

        Args:
            message (str): The message to be streamed.

        Returns:
            Any: The streamed content from the chat chain, or None if the chat chain is not ready.
        """
        if self.chain_with_trimming is None:
            logger.warn("chat chain is not ready")
            return None

        msg = {"input": message, "language": self.language}
        return self.chain_with_trimming.stream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )
