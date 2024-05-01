from enum import Enum


class ResourceSources(Enum):
    PDF = "pdf"
    EXCEL = "excel"
    URL = "url"


class EmbeddingMethods(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
