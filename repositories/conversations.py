from fastapi import HTTPException
from databases.mongo import BaseClient, BaseRepositories
from databases.mongo_dbs import Databases
from models.conversations import Conversation, Ticket


class ConversationRepositories(BaseRepositories):
    def __init__(self) -> None:
        self.client = BaseClient(Databases.MAIN_DB)
        self.collection = Conversation

    def get_list(self, structured=True, **filter_fields):
        objs = self.collection.objects.filter(**filter_fields)

        if structured:
            objs = [obj.to_mongo() for obj in objs]
        return objs

    def get_object(self, structured=True, **filter_fields):
        try:
            obj = self.collection.objects.get(**filter_fields)
        except Exception as exc:
            obj = None

        return obj.to_mongo() if obj and structured else obj

    def create(self, **data):
        obj = self.collection(**data)
        obj.save()
        return obj.to_mongo()


class TicketRepositories(BaseRepositories):
    def __init__(self) -> None:
        self.client = BaseClient(Databases.MAIN_DB)
        self.collection = Ticket

    def get_list(self, structured=True, **filter_fields):
        objs = self.collection.objects.filter(**filter_fields)

        if structured:
            objs = [obj.to_mongo() for obj in objs]
        return objs

    def get_object(self, structured=True, **filter_fields):
        try:
            obj = self.collection.objects.get(**filter_fields)
        except Exception as exc:
            obj = None

        return obj.to_mongo() if obj and structured else obj

    def create(self, **data):
        obj = self.collection(**data)
        obj.save()
        return obj.to_mongo()
