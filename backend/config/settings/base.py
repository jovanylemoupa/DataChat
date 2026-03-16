from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    "django_celery_results",
    # Apps
    "infrastructure.database",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "interfaces.http.middlewares.auth_middleware.KeycloakAuthMiddleware",
    "interfaces.http.middlewares.error_middleware.ErrorHandlerMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "datachat_db",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("DB_HOST", default="postgres"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# Celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_RESULT_EXTENDED = True

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = config("MEDIA_ROOT", default=BASE_DIR / "media")
MAX_UPLOAD_SIZE_MB = config("MAX_UPLOAD_SIZE_MB", default=50, cast=int)

# Keycloak
KEYCLOAK_URL = config("KEYCLOAK_URL")
KEYCLOAK_REALM = config("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = config("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = config("KEYCLOAK_CLIENT_SECRET")

# ChromaDB
CHROMA_HOST = config("CHROMA_HOST", default="chromadb")
CHROMA_PORT = config("CHROMA_PORT", default=8000, cast=int)

# LLM
LLM_PROVIDER = config("LLM_PROVIDER", default="ollama")
OLLAMA_BASE_URL = config("OLLAMA_BASE_URL", default="http://ollama:11434")
OLLAMA_MODEL = config("OLLAMA_MODEL", default="mistral")
GROQ_API_KEY = config("GROQ_API_KEY", default="")
GROQ_MODEL = config("GROQ_MODEL", default="llama-3.1-8b-instant")

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"
