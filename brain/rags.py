from langgraph.graph import END, MessageGraph, StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain.load import dumps, loads
from brain.operations import get_user_documents, get_llm
from brain.prompts import default_template


from dotenv import load_dotenv
from langchain import hub
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Dict, TypedDict, Any, Optional, List, Literal, Union
from langchain.prompts import PromptTemplate
import pprint
import os


# Post-processing
def format_docs(docs: List[Document]) -> str:
    if docs:
        return "\n\n".join(doc.page_content for doc in docs)
    return ""


class GraphState(TypedDict):
    user: Optional[str] = None  # type: ignore
    query: Optional[str] = None  # type: ignore
    context: Optional[str] = None  # type: ignore
    response: Optional[Any] = None  # type: ignore
    direct_to_person: Optional[bool] = False  # type: ignore
    error: Optional[Any] = None  # type: ignore
    resource: Optional[Any] = None # type: ignore


def retriever(state: GraphState) -> Union[dict, str]:
    print("""start retriever()""")

    try:
        query = state.get("query", "")
        user = state.get("user", "")
        docs, resource = get_user_documents(user, query)
        context = format_docs(docs)
        print("context ->> ", len(context))
    except Exception as exc:
        return {"error": {"msg": f"you gor error {exc.args}"}}

    return {"context": context, "resource": resource}


def generator(state: GraphState) -> dict:
    print("""start generator()""")

    try:
        prompt = default_template()
        llm = get_llm()
        context = state.get("context", None)
        query = state.get("query", None)

        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"context": context, "question": query})
    except Exception as exc:
        return {"error": {"msg": f"you gor error {exc.args}"}}

    return {"response": response}


def classifier(state: GraphState) -> dict:
    print("""start classifier()""")
    # TODO check if the user found the answer
    try:
        response = state.get("response", None)
        if response and "NoAnswer" in response:
            # TODO use Langchain Agent & Tools to create a a ticket
            # TODO write  a function to check for answers here and redirect user to a human person.
            return {
                "response": "I cannot answer your question, do you want to create a ticket?",
                "direct_to_person": True,
            }
    except Exception as exc:
        return {"error": {"msg": f"you gor error {exc.args}"}}

    return {}


def finish(state: GraphState) -> dict:
    print("""start finish()""")
    try:
        user = state.get("user", None)
        query = state.get("query", None)
        response = state.get("response", None)
        error = state.get("error", None)
    except Exception as exc:
        return {"error": {"msg": f"you gor error {exc.args}"}}
    return {"response": response, "user": user, "query": query, "error": error}


def continue_next(
    state: GraphState,
) -> Literal["to_generator", "to_finish"]:
    print(f"continue_next: state: {state}")
    context = state.get("context", None)
    error = state.get("error", None)
    response = state.get("response", None)
    if context:
        return "to_generator"

    if response:
        return "to_finish"
    
    if error:
        return "to_finish"

    return "to_finish"


def run_graph_workflow(user, query):

    # prompt = default_template()
    # llm = get_llm()
    # docs = get_user_documents(user, query)
    # context = format_docs(docs)
    # final_chain = {"context": context, "question": query} | prompt | llm | StrOutputParser()

    # def invoke_model(query):
    #     response = final_chain.invoke(query)
    #     return response

    workflow = StateGraph(GraphState)
    """
    # ask question
    # get docs
    # send docs to llm and get the response
    # return response
    
    # complex: add more steps here
    # if the user message  is not in the documents, go back to asking a new question
    # if user want to talk with human , go to next step


    # WorkFlows:
    # - Ask Question -> Get Docs -> LLM Response -> User Message -> over and over again

    # get documents from query and user - retriever
    # call  LLM on the retrieved text - parser
    # check if the answer is found in the documents - classifier
    ---------------------------------------------------------------------
    # if yes, send it to LLM with question to get right answer  - generator
    # if no, ask for another question or talk with a human - classifier
    """

    workflow.add_node("retriever", retriever)
    workflow.add_node("generator", generator)
    workflow.add_node("classifier", classifier)
    workflow.add_node("finish", finish)

    workflow.set_entry_point("retriever")
    workflow.add_edge("generator", "classifier")
    workflow.add_edge("classifier", "finish")
    workflow.add_edge("finish", END)

    workflow.add_conditional_edges(
        source="retriever",
        path=continue_next,
        path_map={
            "to_generator": "generator",
            "to_finish": "finish",
        },
    )

    app = workflow.compile()
    result = app.invoke({"query": query, "user": user})
    print("\n\nResult:\n===============")
    print(result)
    return result
