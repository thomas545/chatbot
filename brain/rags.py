import json
import random
from uuid import uuid4
from typing import TypedDict, Any, Optional, List, Union, Annotated
from operator import add as op_add
from langchain.schema import Document
from langchain_core.tools import tool
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents import create_openai_tools_agent
from langchain.tools.retriever import create_retriever_tool
from brain.operations import get_user_documents, get_llm
from brain.prompts import default_template
from repositories.conversations import TicketRepositories


# Post-processing
def format_docs(docs: List[Document]) -> str:
    if docs:
        return "\n\n".join(doc.page_content for doc in docs)
    return ""


class AgentState(TypedDict):
    user: Optional[str] = None  # type: ignore
    query: Optional[str] = None  # type: ignore
    chat_history: Optional[List] = None  # type: ignore
    resource: Optional[Any] = None  # type: ignore
    llm: Optional[Any] = None  # type: ignore
    search_tool: Optional[Any] = None  # type: ignore
    agent_out: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], op_add]


@tool("create_ticket_tool", return_direct=True)
def create_ticket_tool(query: str, user: str) -> str:
    """when the user complaint or request to create a ticket or talk to human use this tool to
    Create a ticket and returns the ticket's number when the user want to create a ticket.
    use the ticket numer in this return function
    """

    ticket_id = uuid4().hex
    ticket_repo = TicketRepositories()
    ticket_repo.create(
        user_id=user, ticket_ref=ticket_id, subject=query, created_by=user
    )
    return f"#{ticket_id}"


@tool("complaint_tool", return_direct=True)
def complaint_tool(query: str) -> str:
    """In case user is angry or comlaining, try to find the answer for the complaint in the context"""
    return ""


@tool("answer_formatter")
def answer_formatter_tool(answer: str):
    """Returns `answer` directly as output."""
    return answer


def agent_initializer(state: AgentState):
    print("Run agent initializer ...")
    query = state.get("query", "")
    user = state.get("user", "")
    chat_history = state.get("chat_history", "")
    prompt = default_template()
    llm = get_llm()
    retrievers, docs, resource = get_user_documents(user, query, False)
    search_tool = create_retriever_tool(
        retrievers,
        "call_tool",
        "Search for information. you must use this tool!",
    )

    tools = [
        search_tool,
        create_ticket_tool,
        complaint_tool,
        answer_formatter_tool,
    ]

    query_agent_runnable = create_openai_tools_agent(
        llm=llm, tools=tools, prompt=prompt
    )
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_out = query_agent_runnable.invoke(state)

    print("Agent output ->> ", agent_out)
    return {
        "agent_out": agent_out,
        "search_tool": search_tool,
        "llm": llm,
        "resource": resource,
    }


def call_tool(state: AgentState):
    search_tool = state["search_tool"]
    action = state["agent_out"]
    tool_call = action[-1].message_log[-1].additional_kwargs["tool_calls"][-1]

    print("tool_call ->> ", tool_call)
    output = search_tool.invoke(json.loads(tool_call["function"]["arguments"]))
    return {"intermediate_steps": [{"context": str(output)}]}


def resolve_complaint(state: list):
    print("Run execute complaint ->> ")
    action = state["agent_out"]
    print(f"resolve_complaint >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {action}")
    tool_call = action[-1].message_log[-1].additional_kwargs["tool_calls"][-1]
    output = complaint_tool.invoke(json.loads(tool_call["function"]["arguments"]))
    print("resolve_complaint >>>>>>>>>>>>>>>>>>>> OUTPUT \n ", output, "\n")
    return {"intermediate_steps": [{"complaint": str(output)}]}


def complaint_answer(state: list):
    print("> complaint final_answer")
    llm = state["llm"]
    final_answer_llm = llm.bind_tools(
        [answer_formatter_tool], tool_choice="answer_formatter"
    )
    query = state["query"]
    context = state["intermediate_steps"][-1]
    prompt = f"""You are a helpful customer support assistant the user to solve the complaint 
    depend on context but if you don't find the answer in the context 
    you can ask user to create a ticket to talk to human agent.

    context: {context}
    complaint or question: {query}        
    """
    output = final_answer_llm.invoke(prompt)
    function_call = output.additional_kwargs["tool_calls"][-1]["function"]["arguments"]
    return {"agent_out": function_call}


def create_ticket(state: list):
    print("Run create ticket ->> ")
    action = state["agent_out"]
    tool_call = action[-1].message_log[-1].additional_kwargs["tool_calls"][-1]
    arguments = json.loads(tool_call["function"]["arguments"])
    arguments.update({"user": state["user"]})
    output = create_ticket_tool.invoke(arguments)
    return {"intermediate_steps": [{"ticket": str(output)}]}


def ticket_answer(state: list):
    print("> ticket final_answer")
    llm = state["llm"]
    final_answer_llm = llm.bind_tools(
        [answer_formatter_tool], tool_choice="answer_formatter"
    )
    query = state["query"]
    context = state["intermediate_steps"][-1]

    prompt = f"""You are friendly assistant that will reply with the ticket number returned from the
        tool when user want to create a ticket or ask for human help
    reply: {query}        
    CONTEXT: {context}
    your answer should contains the message to the user to tell him the ticket number created 
    and a customer support will contant with it to help ans return the ticket number with message. 
    make the message more readable for human and friendly
    """
    output = final_answer_llm.invoke(prompt)
    function_call = output.additional_kwargs["tool_calls"][-1]["function"]["arguments"]
    return {"agent_out": function_call}


def workflow_results(state: list):
    llm = state["llm"]
    final_answer_llm = llm.bind_tools(
        [answer_formatter_tool], tool_choice="answer_formatter"
    )
    print("> final_answer")
    query = state["query"]
    context = state["intermediate_steps"][-1]["context"]
    print(">>>>>>>>>>>>>> CONTEXT <<<<<<<<<<<<<<<")
    print(context)

    prompt = f"""You are friendly assistant that will answer questions and requests 
        submitted by the user . 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
    CONTEXT: {context}
    QUESTION: {query}            
    """

    # StrOutputParser
    output = final_answer_llm.invoke(prompt)

    print("llm out ->> ", output)

    function_call = output.additional_kwargs["tool_calls"][-1]["function"]["arguments"]
    return {"agent_out": function_call}


def finish(state: AgentState) -> dict:
    print("""start finish()""")
    # try:
    #     user = state.get("user", None)
    #     query = state.get("query", None)
    #     response = state.get("response", None)
    #     error = state.get("error", None)
    # except Exception as exc:
    #     return {"error": {"msg": f"you gor error {exc.args}"}}
    # return {"response": response, "user": user, "query": query, "error": error}

    action = state["agent_out"]
    answer = json.loads(action).get("answer", {})

    return {"response": answer}


def continue_next(state: AgentState):
    print(">>>>>>>>>> router \n ", state, "\n")
    if isinstance(state["agent_out"], list):
        return state["agent_out"][-1].tool
    else:
        return "error"


def handle_error(state: list):
    print("-->>>> handle_error")
    query = state["query"]
    llm = state["llm"]
    final_answer_llm = llm.bind_tools(
        [answer_formatter_tool], tool_choice="answer_formatter"
    )

    prompt = f"""Reply with I don't know, we got an error, 
    try again or ask to talk to customer support person.

    QUESTION: {query}
    """

    output = final_answer_llm.invoke(prompt)
    function_call = output.additional_kwargs[-1]["tool_calls"]["function"]["arguments"]
    return {"agent_out": function_call}
