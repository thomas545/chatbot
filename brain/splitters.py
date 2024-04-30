from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
)


def character_splitter(text, separator="\n", chunk_size=1000, chunk_overlap=200):
    text_splitter = CharacterTextSplitter(
        separator=separator, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(text)
    return docs


def recursive_character_splitter(
    text, separator="\n", chunk_size=1000, chunk_overlap=200
):
    text_splitter = RecursiveCharacterTextSplitter(
        separator=separator, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(text)
    return docs


def recursive_json_splitter(json_obj, max_chunk_size=1000, min_chunk_size=200):
    json_splitter = RecursiveJsonSplitter(
        max_chunk_size=max_chunk_size, min_chunk_size=min_chunk_size
    )
    objs = json_splitter.split_json(
        json_obj,
    )
    docs = json_splitter.create_documents(objs)
    return docs
