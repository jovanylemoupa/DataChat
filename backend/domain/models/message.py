from dataclasses import dataclass
from datetime import datetime
from domain.entities.message_role import MessageRole


@dataclass
class Message:
    id: str
    conversation_id: str
    role: MessageRole
    content: str
    method_explanation: str | None = None
    created_at: datetime | None = None
