from application.dto.resource_dto import ResourceUploadDTO, ResourceResponseDTO
from domain.models.resource import Resource
from domain.repositories.resource_repository import ResourceRepository
from domain.entities.resource_type import ResourceType
from domain.entities.analysis_status import AnalysisStatus
from shared.exceptions.domain_exceptions import InvalidFileTypeError


class UploadResourceUseCase:

    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    def execute(self, dto: ResourceUploadDTO) -> ResourceResponseDTO:
        # 1. Valider le type de fichier
        try:
            resource_type = ResourceType(dto.resource_type)
        except ValueError:
            raise InvalidFileTypeError(dto.resource_type)

        # 2. Créer l'entité domain
        resource = Resource(
            id=None,
            user_id=dto.user_id,
            user_email=dto.user_email,
            name=dto.name,
            resource_type=resource_type,
            file_path=dto.file_path,
            status=AnalysisStatus.PENDING,
            size_bytes=dto.size_bytes,
        )

        # 3. Sauvegarder via le repository
        saved = self.resource_repository.save(resource)

        # 4. Retourner le DTO de réponse
        return ResourceResponseDTO(
            id=saved.id,
            name=saved.name,
            resource_type=saved.resource_type.value,
            status=saved.status.value,
            size_bytes=saved.size_bytes,
            created_at=saved.created_at,
        )