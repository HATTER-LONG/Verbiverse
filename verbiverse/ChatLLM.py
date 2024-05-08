import asyncio
from typing import Any, Dict, List

from langchain.memory import ChatMessageHistory
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough  # 新增
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from LLMServerInfo import getApiKey, getApiUrl, getChatPrompt, getModelName

api_key = getApiKey()
api_url = getApiUrl()

model = getModelName()


class ChatMessageCallBack(BaseCallbackHandler):
    def __init__(self, stream_call_back):
        self.running = False
        self.callBack = stream_call_back

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        print(f"on_llm_start {serialized['name']}")
        self.running = True

    def on_chat_model_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        print(f"on_chat_model_start {serialized['name']}")
        self.running = True

    def on_llm_end(
        self,
        response: LLMResult,
        **kwargs: Any,
    ) -> None:
        print(f"on_llm_end {response}")
        self.running = False

    def on_chat_model_end(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        print(f"on_chat_model_end {serialized['name']}")
        self.running = False

    def is_running(self) -> bool:
        return self.running

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        self.callBack(token)


class ChatChain:
    def __init__(self, callback=None):
        chat = ChatOpenAI(
            model_name=model,
            openai_api_key=api_key,
            openai_api_base=api_url,
            temperature=0.7,
        )
        if callback:
            chat = ChatOpenAI(
                model_name=model,
                openai_api_key=api_key,
                openai_api_base=api_url,
                temperature=0.7,
                streaming=True,
                callbacks=[callback],
            )

        content = getChatPrompt()

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


def print_by_my_callback(message: str):
    print(f"callback message: {message}")


if __name__ == "__main__":
    cb = ChatMessageCallBack(print_by_my_callback)
    chat = ChatChain()
    while True:
        input_string = input("> ")

        msg = {"input": input_string}

        # for chunk in chat.stream(input_string):
        #     print(chunk.content, end="", flush=True)
        asyncio.run(chat.ainvoke(input_string))

        print("cb running {}".format(cb.is_running()))

        print("\n")
