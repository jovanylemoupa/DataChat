from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.llm.llm_client import get_llm
from shared.logger.logger import get_logger

logger = get_logger(__name__)

CLARIFIER_PROMPT = """Tu es un assistant data analyst.

L'utilisateur a posé une question trop vague : "{question}"

Colonnes disponibles dans le fichier : {columns}

Pose UNE seule question courte et précise pour comprendre ce qu'il veut analyser.
Ne propose pas d'options, pose juste la question.

Question de clarification :"""


def clarifier_node(state: AgentState) -> AgentState:
    logger.info(f"Clarifier : question trop vague '{state['question']}'")

    try:
        # Récupérer les colonnes du fichier
        from infrastructure.database.models import Resource as ResourceModel
        import pandas as pd

        resource = ResourceModel.objects.get(id=state["resource_id"])
        df = pd.read_csv(resource.file_path)
        columns = list(df.columns)

        # Générer la question de clarification
        llm = get_llm()
        prompt = CLARIFIER_PROMPT.format(
            question=state["question"],
            columns=columns,
        )
        response = llm.invoke(prompt)
        clarification_question = response.content.strip()

        logger.info(f"Clarifier : question générée = {clarification_question}")

        return {
            **state,
            "needs_clarification": True,
            "clarification_question": clarification_question,
            "final_response": clarification_question,
            "method_explanation": "Question trop vague — clarification demandée",
        }

    except Exception as e:
        logger.error(f"Erreur clarifier : {e}")
        return {**state, "error": str(e)}