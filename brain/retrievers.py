from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from databases.milvus import MilvusLangchainMainRepositories


def create_retrievers(
    docs: List[Document], collection_name: str, embeddings: Embeddings, **kwargs
):
    obj = MilvusLangchainMainRepositories()
    return obj.store_vectors(docs, collection_name, embeddings, **kwargs)


def get_exists_retrievers(collection_name: str, embeddings: Embeddings, **kwargs):
    obj = MilvusLangchainMainRepositories()
    vector_store = obj.get_vectors(collection_name, embeddings, **kwargs)
    return obj.get_retriever(vector_store, search_kwargs={"k": 5})


def get_relevant_documents(retriever, query, **kwargs):
    obj = MilvusLangchainMainRepositories()
    return obj.get_relevant_documents(retriever, query, **kwargs)
