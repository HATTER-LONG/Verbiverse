from langchain_openai import ChatOpenAI, OpenAI
from prompt_ctrl import (
    dump_prompt_template_to_file,
    get_prompt_template,
    load_prompt_template_from_file,
)

api_key = "lm-studio"
api_url = "http://localhost:1234/v1"

model = "Qwen/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q5_k_m.gguf"


prompt_template = get_prompt_template("hardkothari/prompt-maker")

# dump_prompt_template_to_file(prompt_template, "./template.json")

# prompt = load_prompt_template_from_file("./template.json")
print(prompt_template)
chat = OpenAI(
    model_name=model,
    openai_api_key=api_key,
    openai_api_base=api_url,
    temperature=0.7,
)

chain = prompt_template | chat

print(prompt_template.input_variables)

msg = {
    "lazy_prompt": "you are a english teacher, you can help me learn english. What should I do?",
    "task": "learn english",
}

res = chain.invoke(msg)

print(res)
# for r in res:
#     print(r, end="", flush=True)
