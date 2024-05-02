from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from core.schema import ObjectID, MongoModel


class CreateResource(BaseModel):
    # user_id: Optional[str] = None
    source_url: str
    source: str
    collection_name: str
    partition_key: Optional[str] = "user_id"
    partition_name: Optional[str] = None
    embedding_method: str
    user_metadata: Optional[dict] = None
    is_web: Optional[bool] = False
    crawl_pages: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)


class CreateResourceResponse(MongoModel):
    id: Optional[str] = Field(alias="_id")
    user_id: Optional[str] = None
    source_url: Optional[str] = None
    source: Optional[str] = None
    collection_name: Optional[str] = None
    partition_key: Optional[str] = None
    partition_name: Optional[str] = None
    embedding_method: Optional[str] = None
    user_metadata: Optional[dict] = None
    is_web: Optional[bool] = False
    crawl_pages: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

