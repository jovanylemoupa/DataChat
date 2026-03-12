from typing import TypedDict, Annotated
import operator
import pandas as pd


class AgentState(TypedDict):
    # Contexte de la requête
    question: str
    resource_id: str
    resource_type: str  # "csv" | "pdf" | "hybrid"

    # Données chargées
    dataframe: pd.DataFrame | None
    chunks: list[str]

    # Résultats intermédiaires
    route: str  # "csv" | "pdf" | "clarify"
    analysis_result: dict | None
    retrieved_context: list[str]
    needs_clarification: bool
    clarification_question: str | None

    # Mémoire de conversation
    conversation_history: Annotated[list[dict], operator.add]

    # Sortie finale
    final_response: str | None
    method_explanation: str | None
    error: str | None
