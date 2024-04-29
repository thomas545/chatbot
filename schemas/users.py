from typing import Optional, Type, Any, Tuple, Union
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer
from core.schema import MongoModel, ObjectID


class BaseUser(MongoModel):
    username: str
    email: str
    password: str

    # @field_serializer("created_at")
    # def serialize_created_at(self, created_at: datetime, _info):
    #     return int(created_at.timestamp())

    # @field_serializer("updated_at")
    # def serialize_updated_at(self, updated_at: datetime, _info):
    #     return int(updated_at.timestamp())


class UserSignup(BaseUser):
    is_active: bool = True
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)


class UserLogin(BaseUser):
    username: Optional[str] = Field()
    email: Optional[str] = Field()
    password: str


class UserTokenFields(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = Field(default=False)


class UserResponse(MongoModel):
    # id: ObjectID = Field()
    id: Optional[Union[str, ObjectID]] = Field(alias="_id")
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = Field(default=False)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    access_token: Optional[str] = None
