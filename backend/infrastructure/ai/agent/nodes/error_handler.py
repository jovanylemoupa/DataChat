from infrastructure.ai.agent.state import AgentState
from shared.logger.logger import get_logger

logger = get_logger(__name__)


def error_handler_node(state: AgentState) -> AgentState:
    error = state.get("error", "Erreur inconnue")
    logger.error(f"ErrorHandler : {error}")

    if "DoesNotExist" in str(error):
        message = "Le fichier demandé est introuvable."
    elif "read_csv" in str(error) or "pandas" in str(error).lower():
        message = "Impossible de lire le fichier CSV. Vérifiez son format."
    elif "exec" in str(error):
        message = "Impossible d'analyser les données. Reformulez votre question."
    else:
        message = "Une erreur est survenue. Veuillez réessayer."

    return {
        **state,
        "final_response": message,
        "method_explanation": f"Erreur : {error}",
    }