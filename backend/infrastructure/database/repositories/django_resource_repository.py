from domain.models.resource import Resource
from domain.repositories.resource_repository import ResourceRepository
from domain.entities.resource_type import ResourceType
from domain.entities.analysis_status import AnalysisStatus
from infrastructure.database.models import Resource as ResourceModel
from infrastructure.database.models.user_model import UserProfile


class DjangoResourceRepository(ResourceRepository):

    def _get_or_create_user(self, keycloak_id: str, email: str) -> UserProfile:
        profile, _ = UserProfile.objects.get_or_create(
            keycloak_id=keycloak_id,
            defaults={"email": email, "username": email.split("@")[0]},
        )
        return profile

    def save(self, resource: Resource) -> Resource:
        user = self._get_or_create_user(resource.user_id, resource.user_email)
        obj, _ = ResourceModel.objects.update_or_create(
            id=resource.id if resource.id else None,
            defaults={
                "user": user,
                "name": resource.name,
                "resource_type": resource.resource_type.value,
                "file_path": resource.file_path,
                "status": resource.status.value,
                "size_bytes": resource.size_bytes,
            }
        )
        return self._to_domain(obj)

    def find_by_id(self, resource_id: str) -> Resource | None:
        try:
            obj = ResourceModel.objects.get(id=resource_id)
            return self._to_domain(obj)
        except ResourceModel.DoesNotExist:
            return None

    def find_by_user(self, user_id: str) -> list[Resource]:
        objs = ResourceModel.objects.filter(user__keycloak_id=user_id)
        return [self._to_domain(obj) for obj in objs]

    def delete(self, resource_id: str) -> None:
        ResourceModel.objects.filter(id=resource_id).delete()

    def _to_domain(self, obj: ResourceModel) -> Resource:
        """
        Convertit un modèle Django ORM en entité domain pure.
        """
        return Resource(
            id=str(obj.id),
            user_id=str(obj.user.keycloak_id),
            name=obj.name,
            resource_type=ResourceType(obj.resource_type),
            file_path=obj.file_path,
            status=AnalysisStatus(obj.status),
            size_bytes=obj.size_bytes,
            created_at=obj.created_at,
        )