import os
from django.conf import settings


def init_langsmith() -> None:
    """
    Active le tracing LangSmith si LANGCHAIN_TRACING_V2=true.
    Appelé au démarrage de Django (AppConfig.ready).
    """
    if os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true":
        os.environ.setdefault("LANGCHAIN_API_KEY", os.getenv("LANGCHAIN_API_KEY", ""))
        os.environ.setdefault("LANGCHAIN_PROJECT", os.getenv("LANGCHAIN_PROJECT", "datachat"))
        os.environ.setdefault("LANGCHAIN_ENDPOINT", os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"))
