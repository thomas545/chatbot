import json
from langgraph.graph import END, StateGraph
from .rags import (
    AgentState,
    agent_initializer,
    call_tool,
    resolve_complaint,
    complaint_answer,
    create_ticket,
    ticket_answer,
    workflow_results,
    handle_error,
    finish,
    continue_next,
)


def prepare_workflow_response(results: dict):
    """Prepares a JSON-serializable response for the /workflow endpoint."""
    try:
        output = json.loads(results.get("agent_out"))
    except Exception as exc:
        output = results.get("agent_out") or {}
    return {
        "status": "completed",
        "response": output.get("answer", ""),
        "resource": results.get("resource", {}),
    }


def run_graph_workflow(user, query):
    """
    Run the graph workflow of the chatbot and returns a dictionary containing
    the agent response and the next step in the conversation.
    - ask question
    - get docs
    - send docs to llm and get the response
    - return response
    - if user got the complaint or the issue agent will deal with the case and talk to user
    """

    workflow = StateGraph(AgentState)

    # define workflow nodes
    workflow.add_node("agent_initializer", agent_initializer)
    workflow.add_node("call_tool", call_tool)

    workflow.add_node("complaint_tool", resolve_complaint)
    workflow.add_node("complaint_answer", complaint_answer)

    workflow.add_node("create_ticket_tool", create_ticket)
    workflow.add_node("ticket_answer", ticket_answer)

    workflow.add_node("workflow_results", workflow_results)
    workflow.add_node("error", handle_error)
    workflow.add_node("finish", finish)

    # workflow start point
    workflow.set_entry_point("agent_initializer")

    workflow.add_conditional_edges(
        source="agent_initializer",
        path=continue_next,
        path_map={
            "call_tool": "call_tool",
            "complaint_tool": "complaint_tool",
            "create_ticket_tool": "create_ticket_tool",
            "error": "error",
            "finish": "finish",
        },
    )

    # workflow operations and directions
    workflow.add_edge("call_tool", "workflow_results")

    workflow.add_edge("complaint_tool", "complaint_answer")
    workflow.add_edge("complaint_answer", "finish")

    workflow.add_edge("create_ticket_tool", "ticket_answer")
    workflow.add_edge("ticket_answer", "finish")

    workflow.add_edge("workflow_results", "finish")
    workflow.add_edge("error", "finish")

    workflow.add_edge("finish", END)

    app = workflow.compile()
    result = app.invoke({"query": query, "user": user})
    print("\n\nResult:\n===============")
    print(result)
    # output = json.loads(result.get("agent_out"))
    return prepare_workflow_response(result)
