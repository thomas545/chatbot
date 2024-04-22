import os
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Milvus
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

db_connections = {
    "uri": "https://xxxxxx.zillizcloud.com",
    "port": "19530",
    "password": "xxxxxx",
    "user": "xxxxxx",
}
os.environ["OPENAI_API_KEY"] = "sk-xxxxxxx"


def splitter(
    urls: list[str],
    separator: str = "\n",
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
):
    # Text Splitter
    text_splitter = CharacterTextSplitter(
        separator=separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    loaders = UnstructuredURLLoader(urls=urls)
    data_loader = loaders.load()
    docs = text_splitter.split_documents(data_loader)
    return docs


def store_get_vectors(docs: List[Document], collection_name: str) -> Milvus:
    if docs:
        # save emveddings to vector DB
        vector_store = Milvus.from_documents(
            docs,
            OpenAIEmbeddings(),
            collection_name=collection_name,
            connection_args=db_connections,
        )
    else:
        # Get the embeddings from each document.
        vector_store = Milvus(
            OpenAIEmbeddings(),
            collection_name=collection_name,
            connection_args=db_connections,
        )
    print("connect to db ->> ", vector_store)

    return vector_store


def run(question: str, llm: ChatOpenAI, vector_store: Milvus, chat_history: list[str]):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(
        llm, vector_store.as_retriever(), prompt
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )
    document_chain = create_stuff_documents_chain(llm, prompt)

    chain = create_retrieval_chain(retriever_chain, document_chain)

    print("----------------- \n")
    # question = "explain Which MPT-7B model is the bast one?"

    result = chain.invoke({"input": question, "chat_history": []})

    return result
