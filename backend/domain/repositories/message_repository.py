from abc import ABC, abstractmethod
from domain.models.message import Message


class MessageRepository(ABC):

    @abstractmethod
    def save(self, message: Message) -> Message:
        pass

    @abstractmethod
    def find_by_conversation(self, conversation_id: str) -> list[Message]:
        pass
