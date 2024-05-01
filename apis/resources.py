from typing import Annotated
from fastapi import APIRouter, Header, UploadFile, File, Response
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from brain.loaders import DocumentProcessor
from repositories.resources import ResourceRepositories
from schemas.resources import CreateResource, CreateResourceResponse
from databases.milvus import MilvusLangchainMainRepositories, MilvusCollections


ResourcesRouters = APIRouter(prefix="/resources", tags=["resources"])


@ResourcesRouters.post("/create/", response_model=CreateResourceResponse)
async def create_resource_api(
    obj: CreateResource, user: Annotated[str | None, Header()] = None
):
    obj_json = obj.model_dump()
    obj_json["user_id"] = user

    repo = ResourceRepositories()
    resource = repo.create(**obj_json).to_dict()
    resource["_id"] = str(resource["_id"])

    # load documents
    processor = DocumentProcessor(
        resource.get("source", ""),
        RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""], chunk_size=2000, chunk_overlap=200
        ),
    )
    docs = processor.run_loader(resource.get("source_url", ""))

    for doc in docs:
        doc.metadata["user_id"] = str(user)

    milvus = MilvusLangchainMainRepositories()
    milvus.store_vectors(
        docs,
        MilvusCollections.MAIN_COLLECTION,
        OpenAIEmbeddings(),
        partition_key_field=resource["partition_key"],
        index_params={
            "field_name": "vector",
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "index_name": "vector_index",
        },
    )

    return resource
