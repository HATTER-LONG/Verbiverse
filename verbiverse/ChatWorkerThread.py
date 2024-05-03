from PySide6.QtCore import QThread, Signal, Slot


class ChatWorkThread(QThread):
    """
    A QThread subclass for sending messages to LLM and emitting updated content chunks.

    Attributes:
        messageCallBackSignal (Signal[str]): Emitted when a new message chunk is received from the chat.
        stream (bool): Whether to send the message as a streaming or non-streaming operation.

    Methods:
        setChain(chat_chain: ChatWorkChain): Sets the chat chain object for sending messages.
        setMessage(message: str): Sets the message to be sent through the chat chain.
        run(): Starts the thread, sends the message, and emits content chunks if streaming is enabled.
    """

    # Signal for receiving new message chunks
    messageCallBackSignal = Signal(str)

    def __init__(self, stream=True) -> None:
        """
        Initialize a ChatWorkThread instance.

        :param stream: If True, send messages as a stream; otherwise, invoke the chat chain directly.
        """
        super().__init__()
        self.message = None
        self.chat_chain = None
        self.stream = stream

    def setChain(self, chat_chain) -> None:
        """
        Sets the ChatWorkChain object to be used for sending messages.

        :param chat_chain: The ChatWorkChain instance.
        """
        self.chat_chain = chat_chain

    def setMessage(self, message) -> None:
        """
        Sets the message to be sent through the chat chain.

        :param message: The text of the message.
        """
        self.message = message

    @Slot()
    def run(self) -> None:
        """
        Starts the thread, sends the message, and emits content chunks if streaming is enabled.

        If stream is True, sends the message in a streaming manner; otherwise, invokes the chat chain directly.
        """
        if self.chat_chain is None or self.message is None:
            return
        if self.stream:
            content = self.chat_chain.stream(self.message)
            for chunk in content:
                self.messageCallBackSignal.emit(chunk.content)
        else:
            content = self.chat_chain.invoke(self.message)
            self.messageCallBackSignal.emit(
                content
            )  # Changed 'chunk.content' to 'content' since it's not a chunk anymore
