from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, ConfigDict


class ObjectID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Invalid ObjectId")


class MongoModel(BaseModel):
    ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.timestamp(),
            ObjectId: lambda oid: str(oid),
        }
    )
