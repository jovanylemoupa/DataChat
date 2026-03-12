from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResourceUploadDTO:
    """Données reçues lors d'un upload de fichier."""
    name: str
    resource_type: str
    file_path: str
    size_bytes: int
    user_id: str


@dataclass
class ResourceResponseDTO:
    """Données renvoyées après un upload ou une liste."""
    id: str
    name: str
    resource_type: str
    status: str
    size_bytes: int
    created_at: datetime