from abc import ABC, abstractmethod
from domain.models.conversation import Conversation


class ConversationRepository(ABC):

    @abstractmethod
    def save(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    def find_by_id(self, conversation_id: str) -> Conversation | None:
        pass

    @abstractmethod
    def find_by_user(self, user_id: str) -> list[Conversation]:
        pass
