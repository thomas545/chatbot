from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI


from .retrievers import get_exists_retrievers, get_relevant_documents
from repositories.resources import ResourceRepositories

def get_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    return llm

def get_user_documents(user_id, query):
    """Get documents that are relevant to the user's query"""
    repo_obj = ResourceRepositories()
    resource = repo_obj.get_object(user_id=user_id)
    collection_name = resource.get("collection_name")
    embeddings = OpenAIEmbeddings()

    try:
        if resource:
            resource["_id"] = str(resource.get("_id"))
            resource.pop("created_at")
            resource.pop("updated_at")
    except Exception:
        pass

    retrievers = get_exists_retrievers(collection_name, embeddings)
    if not retrievers:
        return []
    
    # Get document ids for all available retrievers
    docs = get_relevant_documents(retrievers, query)
    return docs, resource














