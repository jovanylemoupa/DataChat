from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import EmbeddingFunction


class LocalEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input).tolist()


_embedding_function = None


def get_embedding_function() -> LocalEmbeddingFunction:
    global _embedding_function
    if _embedding_function is None:
        _embedding_function = LocalEmbeddingFunction()
    return _embedding_function