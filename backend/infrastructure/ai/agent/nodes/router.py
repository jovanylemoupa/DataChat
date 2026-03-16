from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.llm.llm_client import get_llm
from shared.logger.logger import get_logger

logger = get_logger(__name__)

VAGUE_KEYWORDS = [
    "analyse", "analyser", "montre", "affiche", "explique",
    "que penses-tu", "dis-moi", "quelque chose", "tout", "overview"
]

ROUTER_PROMPT = """Tu es un agent qui analyse des fichiers de données.

Type de ressource : {resource_type}
Question : {question}

Réponds UNIQUEMENT par un de ces mots :
- "csv" si la question nécessite une analyse précise (calcul, statistique, filtre, comptage)
- "pdf" si la question nécessite une recherche dans un document texte
- "clarify" si la question est vague

Réponse :"""


def router_node(state: AgentState) -> AgentState:
    logger.info(f"Router : analyse de la question '{state['question']}'")

    try:
        question_lower = state["question"].lower().strip()

        # Détection règle-based des questions vagues
        is_vague = (
            len(question_lower.split()) <= 3 or
            any(kw in question_lower for kw in VAGUE_KEYWORDS)
        )

        if is_vague:
            logger.info("Router : question vague détectée → clarify")
            return {**state, "route": "clarify"}

        # Sinon on demande au LLM
        llm = get_llm()
        prompt = ROUTER_PROMPT.format(
            resource_type=state["resource_type"],
            question=state["question"],
        )
        response = llm.invoke(prompt)
        route = response.content.strip().lower()

        if route not in ["csv", "pdf", "clarify"]:
            route = state["resource_type"]

        logger.info(f"Router : route décidée = {route}")
        return {**state, "route": route}

    except Exception as e:
        logger.error(f"Erreur router : {e}")
        return {**state, "route": "error", "error": str(e)}