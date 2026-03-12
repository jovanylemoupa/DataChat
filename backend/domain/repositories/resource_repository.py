from abc import ABC, abstractmethod
from domain.models.resource import Resource


class ResourceRepository(ABC):

    @abstractmethod
    def save(self, resource: Resource) -> Resource:
        pass

    @abstractmethod
    def find_by_id(self, resource_id: str) -> Resource | None:
        pass

    @abstractmethod
    def find_by_user(self, user_id: str) -> list[Resource]:
        pass

    @abstractmethod
    def delete(self, resource_id: str) -> None:
        pass
