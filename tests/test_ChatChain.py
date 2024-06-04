from verbiverse.LLM.ChatChain import ChatChain
import verbiverse.resources.resources_rc

chat = ChatChain()
while True:
    input_string = input("> ")

    for chunk in chat.stream(input_string):
        print(chunk.content, end="", flush=True)

    print("\n")
