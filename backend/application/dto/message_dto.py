from dataclasses import dataclass
from datetime import datetime


@dataclass
class QuestionDTO:
    """Données reçues quand l'utilisateur pose une question."""
    question: str
    resource_id: str
    conversation_id: str | None
    user_id: str


@dataclass
class MessageResponseDTO:
    """Données renvoyées après une réponse de l'agent."""
    id: str
    role: str
    content: str
    method_explanation: str | None
    created_at: datetime