from django.http import JsonResponse
from infrastructure.keycloak.keycloak_client import validate_token


class KeycloakAuthMiddleware:
    """
    Valide le token JWT Keycloak sur chaque requête vers /api/.
    Injecte request.user_id et request.user_email.
    """

    EXEMPT_PATHS = ["/api/health/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        if request.path in self.EXEMPT_PATHS:
            return self.get_response(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Token manquant"}, status=401)

        token = auth_header.split(" ")[1]
        payload = validate_token(token)

        if payload is None:
            return JsonResponse({"error": "Token invalide"}, status=401)

        request.user_id = payload.get("sub")
        request.user_email = payload.get("email")

        return self.get_response(request)
