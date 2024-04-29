from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField
from databases.mongo_dbs import Databases, Collections


class Resource(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.RESOURCES,
    }

    user_id = StringField(db_field="user_id", required=True)
    source_url = StringField(db_field="source_url")
    partition_key = StringField(db_field="partition_key")
    partition_name = StringField(db_field="partition_name")
    embedding_method = StringField(db_field="embedding_method", required=True)
    user_metadata = StringField(db_field="user_metadata")
    is_web = BooleanField(default=False)
    crawl_pages = BooleanField(default=False)
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)