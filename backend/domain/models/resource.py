from dataclasses import dataclass
from datetime import datetime
from domain.entities.resource_type import ResourceType
from domain.entities.analysis_status import AnalysisStatus


@dataclass
class Resource:
    id: str
    user_id: str
    name: str
    resource_type: ResourceType
    file_path: str
    status: AnalysisStatus
    size_bytes: int
    created_at: datetime | None = None
