import verbiverse.resources.resources_rc  # noqa: F401
from verbiverse.LLM.ChatChain import ChatChain

if __name__ == "__main__":
    chat = ChatChain()
    while True:
        input_string = input("> ")

        for chunk in chat.stream(input_string):
            print(chunk.content, end="", flush=True)

        print("\n")
