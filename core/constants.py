from enum import Enum


class ResourceSources(Enum):
    PDF = "pdf"
    EXCEL = "excel"
    URL = "url"


class EmbeddingMethods(Enum):
    OPENAI = "openai"
    GOOGLE = "google"


class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSE = "close"


class TicketPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
