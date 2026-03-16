import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from tasks.file_tasks import process_csv_file, index_pdf_file

from application.use_cases.upload_resource import UploadResourceUseCase
from application.dto.resource_dto import ResourceUploadDTO
from infrastructure.database.repositories.django_resource_repository import DjangoResourceRepository
from interfaces.http.serializers.resource_serializer import ResourceUploadSerializer, ResourceResponseSerializer
from shared.exceptions.domain_exceptions import InvalidFileTypeError
from django.conf import settings


ALLOWED_EXTENSIONS = {"csv", "pdf", "xlsx", "xls"}


class ResourceUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ResourceUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data["file"]

        # Valider l'extension
        ext = file.name.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return Response(
                {"error": f"Extension non supportée : {ext}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Déterminer le type
        if ext == "pdf":
            resource_type = "pdf"
        elif ext in {"xlsx", "xls"}:
            resource_type = "excel"
        else:
            resource_type = "csv"

        # Sauvegarder le fichier
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Exécuter le use case
        try:
            use_case = UploadResourceUseCase(DjangoResourceRepository())
            dto = ResourceUploadDTO(
                name=file.name,
                resource_type=resource_type,
                file_path=file_path,
                size_bytes=file.size,
                user_id=request.user_id,
                user_email=request.user_email or "",
            )
            result = use_case.execute(dto)
        except InvalidFileTypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = ResourceResponseSerializer(result.__dict__)

        # Déclencher le traitement asynchrone
        if resource_type == "csv" or resource_type == "excel":
            process_csv_file.delay(result.id, file_path)
        elif resource_type == "pdf":
            index_pdf_file.delay(result.id, file_path)

        response_serializer = ResourceResponseSerializer(result.__dict__)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ResourceListView(APIView):

    def get(self, request):
        repo = DjangoResourceRepository()
        resources = repo.find_by_user(request.user_id)
        serializer = ResourceResponseSerializer(
            [r.__dict__ for r in resources],
            many=True
        )
        return Response(serializer.data)