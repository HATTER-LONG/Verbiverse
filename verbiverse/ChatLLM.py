from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough  # 新增
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

api_key = "lm-studio"
api_url = "http://localhost:1234/v1"

model = "Qwen/Qwen1.5-7B-Chat-GGUF/qwen1_5-7b-chat-q6_k.gguf"


class ChatChain:
    def __init__(self):
        chat = ChatOpenAI(
            model_name=model,
            openai_api_key=api_key,
            openai_api_base=api_url,
            temperature=0.7,
        )

        content = ""
        with open(
            "/Users/caolei/WorkSpace/Verbiverse/verbiverse/prompt/prompt.txt", "r"
        ) as file:
            content = file.read()

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    content,
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        self.chain = prompt | chat

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


if __name__ == "__main__":
    chat = ChatChain()
    while True:
        input_string = input("> ")

        msg = {"input": input_string}

        for chunk in chat.stream(msg):
            print(chunk.content, end="", flush=True)
        print("\n")
