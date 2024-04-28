from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField
from databases.mongo_dbs import Databases, Collections


class User(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.USERS,
    }

    username = StringField(db_field="username")
    email = StringField(db_field="email")
    password = StringField(db_field="password")
    is_active = BooleanField(db_field="is_active", default=True)
    is_admin = BooleanField(db_field="is_admin", default=False)
    is_verified = BooleanField(db_field="is_verified", default=False)
    last_login = DateTimeField(db_field="last_login")
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)
