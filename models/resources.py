from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, EnumField, DictField
from databases.mongo_dbs import Databases, Collections
from core.constants import ResourceSources, EmbeddingMethods


class Resource(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.RESOURCES,
    }

    user_id = StringField(db_field="user_id", required=True)
    source_url = StringField(db_field="source_url", required=True)
    source = EnumField(db_field="source", enum=ResourceSources, required=True)
    partition_key = StringField(db_field="partition_key")
    partition_name = StringField(db_field="partition_name")
    embedding_method = EnumField(
        db_field="embedding_method", enum=EmbeddingMethods, required=True
    )
    user_metadata = DictField(db_field="user_metadata")
    is_web = BooleanField(db_field="is_web", default=False)
    crawl_pages = BooleanField(db_field="crawl_pages", default=False)
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)
