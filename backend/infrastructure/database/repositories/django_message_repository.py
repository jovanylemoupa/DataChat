from domain.models.message import Message
from domain.entities.message_role import MessageRole
from domain.repositories.message_repository import MessageRepository
from infrastructure.database.models import Message as MessageModel


class DjangoMessageRepository(MessageRepository):

    def save(self, message: Message) -> Message:
        obj = MessageModel.objects.create(
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
            method_explanation=message.method_explanation,
        )
        return self._to_domain(obj)

    def find_by_conversation(self, conversation_id: str) -> list[Message]:
        objs = MessageModel.objects.filter(
            conversation_id=conversation_id
        )
        return [self._to_domain(obj) for obj in objs]

    def _to_domain(self, obj: MessageModel) -> Message:
        return Message(
            id=str(obj.id),
            conversation_id=str(obj.conversation_id),
            role=MessageRole(obj.role),
            content=obj.content,
            method_explanation=obj.method_explanation,
            created_at=obj.created_at,
        )