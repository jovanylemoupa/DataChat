from enum import Enum


class ResourceType(str, Enum):
    CSV = "csv"
    PDF = "pdf"
    EXCEL = "excel"
