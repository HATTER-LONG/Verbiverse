from Functions.Config import cfg
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough  # 新增
from langchain_core.runnables.history import RunnableWithMessageHistory
from LLMServerInfo import getChatPrompt
from ModuleLogger import logger
from OpenAI import getOpenAIChatModel
from qfluentwidgets import qconfig


class ChatChain:
    def __init__(self, callback=None):
        self.chat_prompt = getChatPrompt()
        self.createChatChain()

    def createChatChain(self):
        logger.info("ChatGPT model: %s", qconfig.get(cfg.provider))
        if qconfig.get(cfg.provider) == "openai":
            self.chat = getOpenAIChatModel()
        else:
            raise Exception("Only OpenAI is supported for now")
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
        msg = {"input": message}
        return self.chain_with_trimming.invoke(
            msg,
            {"configurable": {"session_id": "unused"}},
        ).content

    def stream(self, message):
        msg = {"input": message}
        return self.chain_with_trimming.stream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )

    def astream(self, message):
        msg = {"input": message}
        return self.chain_with_trimming.astream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )

    async def ainvoke(self, message):
        msg = {"input": message}
        return await self.chain_with_trimming.ainvoke(
            msg,
            {"configurable": {"session_id": "unused"}},
        )
