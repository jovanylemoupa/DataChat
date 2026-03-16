import chromadb
from django.conf import settings
from infrastructure.ai.agent.state import AgentState
from infrastructure.ai.embeddings.embedding_client import get_embedding_function
from shared.logger.logger import get_logger

logger = get_logger(__name__)


def rag_retriever_node(state: AgentState) -> AgentState:
    logger.info(f"RAGRetriever : recherche pour '{state['question']}'")

    try:
        # 1. Connexion ChromaDB
        client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
        )

        # 2. Récupérer la collection du document
        collection_name = f"resource_{state['resource_id']}"
        collection = client.get_collection(
            name=collection_name,
            embedding_function=get_embedding_function(),
        )

        # 3. Recherche sémantique top-5
        results = collection.query(
            query_texts=[state["question"]],
            n_results=5,
        )

        chunks = results["documents"][0] if results["documents"] else []
        logger.info(f"RAGRetriever : {len(chunks)} chunks trouvés")

        return {**state, "retrieved_context": chunks}

    except Exception as e:
        logger.error(f"Erreur rag_retriever : {e}")
        return {**state, "error": str(e)}