from langgraph.graph import StateGraph, END
from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.agent.nodes.router import router_node
from infrastructure.ai.agent.nodes.data_analyst import data_analyst_node
from infrastructure.ai.agent.nodes.rag_retriever import rag_retriever_node
from infrastructure.ai.agent.nodes.response_formatter import response_formatter_node
from infrastructure.ai.agent.nodes.clarifier import clarifier_node
from infrastructure.ai.agent.nodes.error_handler import error_handler_node


def should_route(state: AgentState) -> str:
    if state.get("error"):
        return "error"
    return state.get("route", "error")


def should_end_or_error(state: AgentState) -> str:
    if state.get("error"):
        return "error"
    return END


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Noeuds
    graph.add_node("router", router_node)
    graph.add_node("data_analyst", data_analyst_node)
    graph.add_node("rag_retriever", rag_retriever_node)
    graph.add_node("clarifier", clarifier_node)
    graph.add_node("response_formatter", response_formatter_node)
    graph.add_node("error_handler", error_handler_node)

    # Point d'entrée
    graph.set_entry_point("router")

    # Routing conditionnel depuis router
    graph.add_conditional_edges(
        "router",
        should_route,
        {
            "csv": "data_analyst",
            "pdf": "rag_retriever",
            "clarify": "clarifier",
            "error": "error_handler",
        },
    )

    # Après data_analyst et rag_retriever → formatter
    graph.add_edge("data_analyst", "response_formatter")
    graph.add_edge("rag_retriever", "response_formatter")

    # Après clarifier → retour au router (attend réponse user)
    graph.add_edge("clarifier", END)

    # Fin du formatter ou erreur
    graph.add_conditional_edges(
        "response_formatter",
        should_end_or_error,
        {
            "error": "error_handler",
            END: END,
        },
    )

    graph.add_edge("error_handler", END)

    return graph.compile()


# Instance globale du graph compilé
agent_graph = build_graph()
