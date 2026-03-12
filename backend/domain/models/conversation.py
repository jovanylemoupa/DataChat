from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Conversation:
    id: str
    user_id: str
    resource_id: str
    title: str
    created_at: datetime | None = None
    messages: list = field(default_factory=list)
