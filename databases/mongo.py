import logging
import pymongo
from bson import ObjectId
from mongoengine import connect, disconnect
from core.environment import get_environ

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, db_name, host=None, **kwargs) -> None:
        self.db = db_name
        if host is None:
            host = get_environ("MONGO_URI")
        self.connetion = connect(db_name, alias=db_name, host=host, **kwargs)

    def close_connection(self):
        return disconnect(self.db)


class BaseRepositories:

    def get_list(self):
        raise NotImplementedError()

    def get_object(self):
        raise NotImplementedError()

    def create(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def patch(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class PyMongoClient:
    def __init__(self, database_name: str, uri: str = ""):
        self.URI = get_environ("MONGO_URI") or uri
        self.client = pymongo.MongoClient(self.URI)
        # self.database = database_name

        logger.info(f"Mongo Connected: {self.client}")


class MainRepositories:
    def __init__(
        self, db_name: str, collection_name: str, client: PyMongoClient = None
    ):
        self.database = db_name
        self.collection = collection_name
        self.client = client or PyMongoClient(db_name)

    def insert_one(self, data, **kwargs):
        logger.info("insert_one", data, kwargs)
        return (
            self.client[self.database][self.collection]
            .insert_one(data, **kwargs)
            .inserted_id
        )

    def insert_many(self, data, **kwargs):
        logger.info("insert_many", data, kwargs)
        return (
            self.client[self.database][self.collection]
            .insert_many(data, **kwargs)
            .inserted_ids
        )

    def find_one(self, query, **kwargs):
        logger.info("find_one", query, kwargs)
        return self.client[self.database][self.collection].find_one(query, **kwargs)

    def count(self, query, **kwargs):
        logger.info("count", query, kwargs)
        return self.client[self.database][self.collection].count_documents(
            query, **kwargs
        )

    def find(self, query, skip=0, limit=None, sort=None, **kwargs):
        logger.info("find", query, kwargs)
        if sort:
            if limit:
                return (
                    self.client[self.database][self.collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .sort(sort)
                    .limit(limit)
                )
            else:
                return (
                    self.client[self.database][self.collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .sort(sort)
                )
        else:
            if limit:
                return (
                    self.client[self.database][self.collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .limit(limit)
                )
            else:
                return (
                    self.client[self.database][self.collection]
                    .find(query, **kwargs)
                    .skip(skip)
                )

    def find_one_and_update(self, query, update_query, **kwargs):
        logger.info("find_one_and_update", query, kwargs)
        return self.client[self.database][self.collection].find_one_and_update(
            query, update_query, **kwargs
        )

    def update_one(self, query, update_query, **kwargs):
        logger.info("update_one", query, kwargs)
        return self.client[self.database][self.collection].update_one(
            query, update_query, **kwargs
        )

    def update_many(self, query, update_query, **kwargs):
        logger.info("update_many", query, kwargs)
        return self.client[self.database][self.collection].update_many(
            query, update_query, **kwargs
        )

    def delete_one(self, query, **kwargs):
        logger.info("update_many", query, kwargs)
        return self.client[self.database][self.collection].delete_one(query, **kwargs)

    def delete_many(self, query, **kwargs):
        logger.info("delete_many", query, kwargs)
        return self.client[self.database][self.collection].delete_many(query, **kwargs)

    @staticmethod
    def is_valid_id(_id):
        return ObjectId().is_valid(_id)
