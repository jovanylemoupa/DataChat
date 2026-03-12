class AgentError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Erreur agent IA : {message}")


class EmbeddingError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Erreur embedding : {message}")


class LLMError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Erreur LLM : {message}")
