from Functions.Config import cfg
from Functions.SignalBus import signalBus
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from LLMServerInfo import getChatPrompt
from ModuleLogger import logger
from OpenAI import getOpenAIChatModel
from qfluentwidgets import qconfig
from TongYiQWen import getTongYiChatModel


class ChatChain:
    def __init__(self):
        self.chat_prompt = getChatPrompt()
        self.createChatChain()

        signalBus.llm_config_change_signal.connect(self.createChatChain)

    def createChatChain(self) -> None:
        self.chain_with_trimming = None
        provider = qconfig.get(cfg.provider)
        logger.info("provider is: %s", provider)
        logger.info("chat model is: %s", qconfig.get(cfg.model_name))
        try:
            if provider == "openai":
                self.chat = getOpenAIChatModel()
            elif provider == "tongyi":
                self.chat = getTongYiChatModel()
            else:
                raise Exception(f"Not supported {provider} for now")
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

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
        stored_messages = self.demo_ephemeral_chat_history_for_chain.messages
        if len(stored_messages) <= 10:
            return False

        self.demo_ephemeral_chat_history_for_chain.clear()
        for message in stored_messages[-10:]:
            self.demo_ephemeral_chat_history_for_chain.add_message(message)

        return True

    def invoke(self, message):
        if self.chain_with_trimming is None:
            logger.warn("chat chain is not ready")
            return
        msg = {"input": message}
        return self.chain_with_trimming.invoke(
            msg,
            {"configurable": {"session_id": "unused"}},
        ).content

    def stream(self, message):
        if self.chain_with_trimming is None:
            logger.warn("chat chain is not ready")
            return
        msg = {"input": message}
        return self.chain_with_trimming.stream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )
