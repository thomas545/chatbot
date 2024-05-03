from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from core.schema import ObjectID, MongoModel


class StartConversation(BaseModel):
    query: str

