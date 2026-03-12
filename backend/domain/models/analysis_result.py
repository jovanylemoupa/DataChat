from dataclasses import dataclass
from domain.entities.analysis_status import AnalysisStatus


@dataclass
class AnalysisResult:
    resource_id: str
    status: AnalysisStatus
    result: dict | None = None
    error: str | None = None
