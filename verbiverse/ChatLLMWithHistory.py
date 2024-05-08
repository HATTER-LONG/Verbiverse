from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from LLMServerInfo import getApiKey, getApiUrl, getCheckPrompt, getModelName


class ChatLLMWithHistory:
    def __init__(self):
        chat = ChatOpenAI(
            model_name=getModelName(),
            openai_api_key=getApiKey(),
            openai_api_base=getApiUrl(),
            temperature=0.7,
        )

        content = getCheckPrompt()

        prompt = PromptTemplate.from_template(content)

        self.chain = prompt | chat
        self.chat_history_for_chain = None

    def setChatHistoryForChain(self, chat_message_history):
        self.chat_history_for_chain = str(chat_message_history)

    def stream(self, message):
        msg = {"data": message, "history": self.chat_history_for_chain}
        return self.chain.stream(msg)
