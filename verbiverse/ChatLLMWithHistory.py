from langchain_core.prompts import PromptTemplate
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
        # TODO: 修改硬编码路径
        with open(
            "/Users/caolei/WorkSpace/Verbiverse/verbiverse/prompt/check_CN.txt", "r"
        ) as file:
            content = file.read()
        prompt = PromptTemplate.from_template(content)

        self.chain = prompt | chat
        self.chat_history_for_chain = None

    def setChatHistoryForChain(self, chat_message_history):
        self.chat_history_for_chain = str(chat_message_history)

    def stream(self, message):
        msg = {"data": message, "history": self.chat_history_for_chain}
        return self.chain.stream(msg)
