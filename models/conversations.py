from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    CASCADE,
)
from databases.mongo_dbs import Databases, Collections
from .resources import Resource


class Conversation(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.CONVERSATIONS,
    }

    user_id = StringField(db_field="user_id", required=True)
    resource_id = ReferenceField(
        Resource, db_field="resource_id", required=True, reverse_delete_rule=CASCADE
    )
    query = StringField(db_field="query")
    response = StringField(db_field="response")
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)
