from django.conf import settings
from langchain_core.language_models import BaseChatModel


def get_llm() -> BaseChatModel:
    """
    Retourne le client LLM configuré selon LLM_PROVIDER.
    Ollama (local) par défaut, OpenAI en option.
    """
    provider = settings.LLM_PROVIDER

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.1,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
        )

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.1,
        )

    raise ValueError(f"LLM_PROVIDER inconnu : {provider}")
