from tasks.celery import app
from shared.logger.logger import get_logger

logger = get_logger(__name__)


@app.task(bind=True, max_retries=3)
def process_csv_file(self, resource_id: str, file_path: str):
    """
    Tâche asynchrone : profiling complet d'un fichier CSV.
    TODO: implémenter avec csv_pipeline.py
    """
    logger.info(f"Traitement CSV : resource_id={resource_id}")


@app.task(bind=True, max_retries=3)
def index_pdf_file(self, resource_id: str, file_path: str):
    """
    Tâche asynchrone : extraction + chunking + indexation ChromaDB d'un PDF.
    TODO: implémenter avec rag_pipeline.py
    """
    logger.info(f"Indexation PDF : resource_id={resource_id}")
