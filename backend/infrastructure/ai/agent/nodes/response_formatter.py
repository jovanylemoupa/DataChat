from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.llm.llm_client import get_llm
from shared.logger.logger import get_logger

logger = get_logger(__name__)

FORMATTER_PROMPT = """Tu es un assistant data analyst. Tu expliques des résultats d'analyse de données.

Question posée : {question}
Résultat de l'analyse : {result}
Code utilisé : {code}
Historique de conversation : {history}

Réponds en français de manière claire et concise.
- Explique le résultat en langage naturel
- Mentionne les chiffres importants
- Sois précis mais accessible

Réponse :"""

FORMATTER_PROMPT_PDF = """Tu es un assistant qui répond aux questions sur des documents.

Question posée : {question}
Contexte extrait du document : {context}
Historique de conversation : {history}

Réponds en français de manière claire et concise en te basant uniquement sur le contexte fourni.

Réponse :"""


def response_formatter_node(state: AgentState) -> AgentState:
    logger.info("ResponseFormatter : génération de la réponse finale")

    try:
        llm = get_llm()

        # Réponse pour analyse CSV
        if state.get("analysis_result"):
            prompt = FORMATTER_PROMPT.format(
                question=state["question"],
                result=state["analysis_result"].get("result", ""),
                code=state["analysis_result"].get("code", ""),
                history=_format_history(state["conversation_history"]),
            )
            method = f"Code Pandas exécuté :\n{state['analysis_result'].get('code', '')}"

        # Réponse pour RAG PDF
        else:
            prompt = FORMATTER_PROMPT_PDF.format(
                question=state["question"],
                context="\n".join(state.get("retrieved_context", [])),
                history=_format_history(state["conversation_history"]),
            )
            method = "Recherche sémantique dans le document"

        response = llm.invoke(prompt)

        return {
            **state,
            "final_response": response.content.strip(),
            "method_explanation": method,
        }

    except Exception as e:
        logger.error(f"Erreur response_formatter : {e}")
        return {**state, "error": str(e)}


def _format_history(history: list) -> str:
    """Formate l'historique pour le prompt."""
    if not history:
        return "Aucun historique"
    return "\n".join([f"{m['role']}: {m['content']}" for m in history[-4:]])