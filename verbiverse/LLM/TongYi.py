from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi

llm = ChatTongyi()

llm.model_name = "qwen1.5-110b-chat"

for chunk in llm.stream("你的模型尺寸是多少"):
    print(chunk.content, end="", flush=True)
