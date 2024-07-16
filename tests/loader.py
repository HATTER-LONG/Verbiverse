# from langchain_core.documents import Document
path = "~/Desktop/资料/文档/Magic Tree House 神奇树屋01-55（MOBI+PDF+MP3）/01 Dinosaurs Before Dark - Mary Pope Osborne[www.oiabc.com]/01 Dinosaurs Before Dark - Mary Pope Osborne.pdf"


# def llamaIndexWithLmStudio():
#     from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
#     from llama_index.embeddings.openai import OpenAIEmbedding

#     # documents = SimpleDirectoryReader(input_files=list(path)).load_data()
#     # print(documents)
#     print("1111")
#     embed_model = OpenAIEmbedding(
#         # model="mixedbread-ai/mxbai-embed-large-v1",
#         api_base="http://localhost:1234/v1",
#         api_key="lm-studio",
#     )
#     print("2222")
#     Settings.embed_model = embed_model
#     print("3333")
#     embeddings = embed_model.get_text_embedding(
#         "Open AI new Embeddings models is awesome."
#     )
#     print(embeddings[:5])
#   # index = VectorStoreIndex.from_documents(documents)


def pdfLoader():
    from langchain_community.document_loaders import PyPDFLoader

    ret = PyPDFLoader(path)
    page = ret.load()
    print(len(page))
    return page


def langchainWithOpenAI():
    import hashlib
    import os

    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    embed = OpenAIEmbeddings(
        model="mixedbread-ai/mxbai-embed-large-v1",
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="lm-studio",
        check_embedding_ctx_length=False,
    )
    md5_path = (
        "./app/database/" + str(hashlib.md5(path.encode("utf-8")).hexdigest()) + "_db"
    )

    db = None
    if not os.path.exists(md5_path):
        print("create a new db")

        docs = pdfLoader()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        db = Chroma.from_documents(
            documents=splits,
            embedding=embed,
            persist_directory=md5_path,
        )
    else:
        print("load a db")
        db = Chroma(persist_directory=md5_path, embedding_function=embed)
    # # ret = db.similarity_search("who is jack?", k=4)
    # print(ret)

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model_name="Qwen/Qwen2-7B-Instruct-GGUF",
        openai_api_key="lm-studio",
        openai_api_base="http://localhost:1234/v1",
        temperature=0.7,
    )
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 4})
    retriever = db.as_retriever(search_kwargs={"k": 4})
    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    results = rag_chain.invoke({"input": "这个故事讲了什么?"})
    print(results)


# llamaIndexWithLmStudio()
langchainWithOpenAI()
