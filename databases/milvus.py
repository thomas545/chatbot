import os
import logging
from typing import List, Union, Any
from pymilvus import connections, CollectionSchema

from langchain_community.vectorstores import Milvus
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


logger = logging.getLogger(__name__)


class MilvusCollections:
    MAIN_COLLECTION = "mainBot"


class MilvusClient:
    def __init__(
        self,
        uri: str = None,
        port: str = None,
        user: str = None,
        password: str = None,
    ) -> None:
        self.uri = uri or os.environ.get("MILVUS_URI")
        self.port = port or os.environ.get("MILVUS_PORT")
        self.user = user or os.environ.get("MILVUS_USER")
        self.password = password or os.environ.get("MILVUS_PASSWORD")

    def client_connect(self):
        if not any([self.uri, self.port]):
            raise ValueError("Neither MILVUS_URI nor MILVUS_PORT is set.")
        try:
            connections.connect(
                uri=f"{self.uri}:{self.port}",
                user=self.user,
                password=self.password,
            )
            logger.info("Milvus client connected")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False

    def close_connection(self):
        connections.close_all()


class MilvusMainRepositories:

    def __init__(self) -> None:
        self.client = MilvusClient()
        # initialize connection
        self.client.client_connect()

    def create_collection(
        self, collection_name: str, schema: CollectionSchema, dimension: int = 128
    ):
        # Create collection
        collection = self.client.create_collection(collection_name, schema)
        return collection

    def insert_data(self, collection_name, data):
        # Insert data into collection
        collection = self.client.collection(collection_name)
        ids = collection.insert(data)
        collection.flush()

        return ids

    def delete_data(self, collection_name, ids):
        # Delete vectors from collection by ids
        collection = self.client.collection(collection_name)
        collection.delete(ids)

    def create_index(
        self, collection_name, field_name="embedding", index_type="IVF_FLAT", nlist=2048
    ):
        # Create index for the specified collection and field
        collection = self.client.collection(collection_name)
        index_param = {"nlist": nlist}
        index = collection.create_index(field_name, index_type, index_param)

        return index

    def index_data(self, collection_name):
        # Index data in the specified collection
        collection = self.client.collection(collection_name)
        collection.load()
        collection.build_index()


class MilvusLangchainMainRepositories:
    def __init__(self) -> None:
        self.CLIENT = MilvusClient()
        self.MILVUS_CONNECTION = {
            "uri": self.CLIENT.uri,
            "port": self.CLIENT.port,
            "user": self.CLIENT.user,
            "password": self.CLIENT.password,
        }
        # self.DEFAULT_MILVUS_CONNECTION = {
        #     "host": "localhost",
        #     "port": "19530",
        #     "user": "",
        #     "password": "",
        #     "secure": False,
        # }

    def store_vectors(
        self,
        docs: List[Document],
        collection_name: str,
        embeddings: Embeddings,
        **kwargs,
    ) -> Milvus:
        # save emveddings to vector DB
        logger.info("storing docs ....")
        vector_store = Milvus.from_documents(
            docs,
            embeddings,
            collection_name=collection_name,
            connection_args=self.MILVUS_CONNECTION,
            **kwargs,
        )

        return vector_store

    def get_vectors(
        self, collection_name: str, embeddings: Embeddings, **kwargs
    ) -> Milvus:
        # Get the embeddings from each document.
        vectors = Milvus(
            embeddings,
            collection_name=collection_name,
            connection_args=self.MILVUS_CONNECTION,
            **kwargs,
        )
        return vectors

    def search_similarity(
        self, vector_db: Milvus, query: Union[str, Any]
    ) -> List[Document]:
        docs = vector_db.similarity_search(query)
        return docs

    def get_retriever(
        self, vectors: Milvus, search_kwargs: dict = {"k": 5}
    ) -> VectorStoreRetriever:
        retriever = vectors.as_retriever(search_kwargs=search_kwargs)
        return retriever

    def get_relevant_documents(
        self, retriever: VectorStoreRetriever, query: str
    ) -> List[Document]:
        docs = retriever.get_relevant_documents(query)
        return docs
