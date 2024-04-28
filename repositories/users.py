from fastapi import HTTPException
from mongoengine import Document
from databases.mongo import BaseClient, BaseRepositories
from databases.mongo_dbs import Databases
from models.users import User


class UserRepositories(BaseRepositories):
    def __init__(self) -> None:
        self.client = BaseClient(Databases.MAIN_DB)
        self.collection = User

    def get_list(self, structured=True, **filter_fields):
        objs = self.collection.objects.filter(**filter_fields)

        if structured:
            objs = [obj.to_mongo() for obj in objs]
        return objs

    def get_object(self, structured=True, **filter_fields):
        try:
            obj = self.collection.objects.get(**filter_fields)
        except Exception as exc:
            raise HTTPException(404, "Object Not Found")

        return obj.to_mongo() if structured else obj

    def create(self, collection: Document, **data):
        obj = collection(**data)  # type: ignore
        obj.save()
        return obj.to_mongo()
