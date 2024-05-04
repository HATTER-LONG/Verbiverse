from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from LLMServerInfo import get_api_key, get_api_url, get_model


class ChatLLMWithHistory:
    def __init__(self):
        chat = ChatOpenAI(
            model_name=get_model(),
            openai_api_key=get_api_key(),
            openai_api_base=get_api_url(),
            temperature=0.7,
        )

        content = ""
        with open(
            "/Users/caolei/WorkSpace/Verbiverse/verbiverse/prompt/check_CN.txt", "r"
        ) as file:
            content = file.read()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    content,
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "<data>{input}<data>"),
            ]
        )

        self.chain = prompt | chat

        self.chat_history_for_chain = ChatMessageHistory()

        self.chain_with_message_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.chat_history_for_chain,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def setChatHistoryForChain(self, chat_message_history):
        self.chat_history_for_chain.clear()
        self.chat_history_for_chain.add_messages(chat_message_history.messages)

    def stream(self, message):
        msg = {"input": message}
        return self.chain_with_message_history.stream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )


if __name__ == "__main__":
    chat_llm = ChatLLMWithHistory()
    while True:
        input_string = input("> ")

        for chunk in chat_llm.stream(input_string):
            print(chunk.content, end="", flush=True)
        print("\n")
        print(chat_llm.chat_history_for_chain.messages)
        print("\n")
