import jwt
from django.conf import settings
from keycloak import KeycloakOpenID
from shared.logger.logger import get_logger

logger = get_logger(__name__)

_keycloak_client: KeycloakOpenID | None = None


def get_keycloak_client() -> KeycloakOpenID:
    global _keycloak_client
    if _keycloak_client is None:
        _keycloak_client = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            realm_name=settings.KEYCLOAK_REALM,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
        )
    return _keycloak_client


def validate_token(token: str) -> dict | None:
    """
    Valide un token JWT Keycloak.
    Retourne le payload décodé ou None si invalide.
    """
    try:
        client = get_keycloak_client()
        public_key = client.public_key()
        options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
        payload = jwt.decode(
            token,
            f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----",
            algorithms=["RS256"],
            options=options,
        )
        return payload
    except Exception as e:
        logger.error(f"Token invalide : {e}")
        return None
