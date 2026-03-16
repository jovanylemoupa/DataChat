import pandas as pd
from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.llm.llm_client import get_llm
from shared.logger.logger import get_logger

logger = get_logger(__name__)

DATA_ANALYST_PROMPT = """Tu es un expert data analyst. Tu analyses des données CSV avec Pandas.

Colonnes disponibles : {columns}
Échantillon des données :
{sample}

Question : {question}

Écris UNIQUEMENT le code Python Pandas pour répondre à cette question.
- Utilise `df` comme variable du DataFrame
- Retourne le résultat dans une variable `result`
- Code simple, pas de import, pas d'explication

Code :"""


def data_analyst_node(state: AgentState) -> AgentState:
    logger.info(f"DataAnalyst : traitement de '{state['question']}'")

    try:
        # 1. Charger le DataFrame depuis le fichier
        from infrastructure.database.models import Resource as ResourceModel
        resource = ResourceModel.objects.get(id=state["resource_id"])
        df = pd.read_csv(resource.file_path)

        # 2. Demander au LLM de générer le code Pandas
        llm = get_llm()
        prompt = DATA_ANALYST_PROMPT.format(
            columns=list(df.columns),
            sample=df.head(3).to_string(),
            question=state["question"],
        )
        response = llm.invoke(prompt)
        code = _extract_code(response.content)
        logger.info(f"Code généré : {code}")

        # 3. Exécuter le code généré
        local_vars = {"df": df, "result": None}
        exec(code, {}, local_vars)
        result = local_vars.get("result")

        analysis_result = {
            "code": code,
            "result": str(result),
            "columns": list(df.columns),
            "row_count": len(df),
        }

        return {**state, "analysis_result": analysis_result, "dataframe": df}

    except Exception as e:
        logger.error(f"Erreur data_analyst : {e}")
        return {**state, "error": str(e)}


def _extract_code(llm_response: str) -> str:
    """Extrait le code Python de la réponse du LLM."""
    if "```python" in llm_response:
        code = llm_response.split("```python")[1].split("```")[0]
    elif "```" in llm_response:
        code = llm_response.split("```")[1].split("```")[0]
    else:
        code = llm_response
    return code.strip()