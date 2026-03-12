from django.http import JsonResponse
from shared.exceptions.domain_exceptions import ResourceNotFoundError, InvalidFileTypeError
from shared.logger.logger import get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ResourceNotFoundError):
            return JsonResponse({"error": str(exception)}, status=404)

        if isinstance(exception, InvalidFileTypeError):
            return JsonResponse({"error": str(exception)}, status=400)

        logger.error("Erreur non gérée", exc_info=exception)
        return JsonResponse({"error": "Erreur interne du serveur"}, status=500)
