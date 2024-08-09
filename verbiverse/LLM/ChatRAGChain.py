import hashlib
import os

from Functions.Config import cfg
from Functions.LoadPdfText import PdfReader
from Functions.SignalBus import signalBus
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from LLMServerInfo import (
    getChatModelByCfg,
    getEmbedModelByCfg,
    getTargetLanguage,
)
from ModuleLogger import logger
from pebble import concurrent


@concurrent.thread
def loadDatabase(database_path, pdf_reader, embed):
    if not os.path.exists(database_path):
        logger.info(f"create embed db [{database_path}]")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(pdf_reader.pages)
        return Chroma.from_documents(
            documents=splits,
            embedding=embed,
            persist_directory=database_path,
        )
    else:
        logger.info(f"load embed db [{database_path}]")
        return Chroma(persist_directory=database_path, embedding_function=embed)


class ChatRAGChain:
    """Chat LLM RAG"""

    def __init__(self, pdf_reader: PdfReader):
        logger.info(f"database path {cfg.get(cfg.database_folder)}")
        filename_md5 = (
            str(hashlib.md5(pdf_reader.pdf_path.encode("utf-8")).hexdigest()) + "_db"
        )
        logger.info(f"pdf database name: [{pdf_reader.pdf_path}] -> [{filename_md5}]")
        self.database_path = cfg.get(cfg.database_folder) + "/" + filename_md5

        self.pdf_reader = pdf_reader
        self.createChatChain()
        self.stored_messages = {}
        signalBus.llm_config_change_signal.connect(self.createChatChain)

    def embedding(self) -> None:
        self.embed = getEmbedModelByCfg()
        return loadDatabase(self.database_path, self.pdf_reader, self.embed).result()
        # if not os.path.exists(self.database_path):
        #     logger.info(f"create embed db [{self.database_path}]")
        #     text_splitter = RecursiveCharacterTextSplitter(
        #         chunk_size=1000, chunk_overlap=200
        #     )
        #     splits = text_splitter.split_documents(self.pdf_reader.pages)
        #     return Chroma.from_documents(
        #         documents=splits,
        #         embedding=self.embed,
        #         persist_directory=self.database_path,
        #     )
        # else:
        #     logger.info(f"load embed db [{self.database_path}]")
        #     return Chroma(
        #         persist_directory=self.database_path, embedding_function=self.embed
        #     )

    def createChatChain(self) -> None:
        """
        A function that creates a chat chain by initializing various attributes and objects.
        This function sets up the chat model, target language, chat prompt, and message history for the chain.
        It then creates a chain with message history and applies trimming functionality to it.
        """
        signalBus.status_signal.emit("Embedding PDF", "Please wait!!")
        self.db = self.embedding()
        signalBus.status_signal.emit("Embedding PDF", "Embedding finished!!")
        self.rag_chain = None
        try:
            self.chat = getChatModelByCfg()
        except Exception as e:
            logger.error("get chat model error: %s", e)
            return

        self.language = getTargetLanguage()
        # self.chat_prompt = getChatPrompt()
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        retriever = self.db.as_retriever(search_kwargs={"k": 2})
        history_aware_retriever = create_history_aware_retriever(
            self.chat, retriever, contextualize_q_prompt
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know. Use three sentences maximum and keep the "
                    "answer concise."
                    "\n\n"
                    "{context}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.chat, self.prompt)

        self.rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # self.chain = self.prompt | self.chat

        self.demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

        self.chain_with_message_history = RunnableWithMessageHistory(
            self.rag_chain,
            lambda session_id: self.demo_ephemeral_chat_history_for_chain,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        self.chain_with_trimming = (
            RunnablePassthrough.assign(messages_trimmed=self.trim_messages)
            | self.chain_with_message_history
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.stored_messages:
            self.stored_messages[session_id] = ChatMessageHistory()
        return self.stored_messages[session_id]

    def trim_messages(self, jchain_input):
        """
        Trims the messages in the `demo_ephemeral_chat_history_for_chain` attribute to the last 10 messages.

        Args:
            jchain_input (Any): The input for the function. Currently not used.

        Returns:
            bool: True if the messages were successfully trimmed, False otherwise.
        """
        stored_messages = self.demo_ephemeral_chat_history_for_chain.messages
        if len(stored_messages) <= 10:
            return False

        self.demo_ephemeral_chat_history_for_chain.clear()
        for message in stored_messages[-10:]:
            self.demo_ephemeral_chat_history_for_chain.add_message(message)

        return True

    def invoke(self, message):
        """
        Invokes the chat chain with the given message.

        Args:
            message (str): The message to be sent to the chat chain.

        Returns:
            str or None: The content of the response from the chat chain, or None if the chat chain is not ready.
        """
        if self.chain_with_trimming is None:
            logger.warn("chat chain is not ready")
            return None
        msg = {"input": message}
        return self.chain_with_trimming.invoke(
            msg,
            {"configurable": {"session_id": "unused"}},
        ).content

    def stream(self, message):
        """
        Stream the given message through the chat chain.

        Args:
            message (str): The message to be streamed.

        Returns:
            Any: The streamed content from the chat chain, or None if the chat chain is not ready.
        """
        if self.chain_with_message_history is None:
            logger.warn("chat chain is not ready")
            return None

        msg = {"input": message, "language": self.language}
        print(msg)
        return self.chain_with_message_history.stream(
            msg,
            {"configurable": {"session_id": "unused"}},
        )
