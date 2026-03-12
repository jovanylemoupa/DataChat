from domain.models.conversation import Conversation
from domain.repositories.conversation_repository import ConversationRepository
from infrastructure.database.models import Conversation as ConversationModel


class DjangoConversationRepository(ConversationRepository):

    def save(self, conversation: Conversation) -> Conversation:
        obj, _ = ConversationModel.objects.update_or_create(
            id=conversation.id if conversation.id else None,
            defaults={
                "user_id": conversation.user_id,
                "resource_id": conversation.resource_id,
                "title": conversation.title,
            }
        )
        return self._to_domain(obj)

    def find_by_id(self, conversation_id: str) -> Conversation | None:
        try:
            obj = ConversationModel.objects.get(id=conversation_id)
            return self._to_domain(obj)
        except ConversationModel.DoesNotExist:
            return None

    def find_by_user(self, user_id: str) -> list[Conversation]:
        objs = ConversationModel.objects.filter(
            user__keycloak_id=user_id
        ).select_related("resource")
        return [self._to_domain(obj) for obj in objs]

    def _to_domain(self, obj: ConversationModel) -> Conversation:
        return Conversation(
            id=str(obj.id),
            user_id=str(obj.user.keycloak_id),
            resource_id=str(obj.resource_id),
            title=obj.title,
            created_at=obj.created_at,
        )