import os
from tasks.celery import app
from infrastructure.ai.pipelines.csv_pipeline import profile_csv
from shared.logger.logger import get_logger

logger = get_logger(__name__)


@app.task(bind=True, max_retries=3)
def process_csv_file(self, resource_id: str, file_path: str):
    """
    Tâche asynchrone : profiling complet d'un fichier CSV avec Pandas.
    Met à jour le status de la Resource en base.
    """
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    django.setup()

    from infrastructure.database.models import Resource as ResourceModel

    try:
        # 1. Mettre le status à "running"
        ResourceModel.objects.filter(id=resource_id).update(status="running")
        logger.info(f"Traitement CSV démarré : resource_id={resource_id}")

        # 2. Profiler le CSV avec Pandas
        profile = profile_csv(file_path)

        # 3. Mettre le status à "done"
        ResourceModel.objects.filter(id=resource_id).update(status="done")
        logger.info(f"Traitement CSV terminé : resource_id={resource_id}")

        return profile

    except Exception as exc:
        # 4. En cas d'erreur → status "failed" + retry
        ResourceModel.objects.filter(id=resource_id).update(status="failed")
        logger.error(f"Erreur traitement CSV : {exc}")
        raise self.retry(exc=exc, countdown=5)


@app.task(bind=True, max_retries=3)
def index_pdf_file(self, resource_id: str, file_path: str):
    """
    Tâche asynchrone : extraction + chunking + indexation ChromaDB d'un PDF.
    TODO: implémenter avec rag_pipeline.py
    """
    logger.info(f"Indexation PDF : resource_id={resource_id}")