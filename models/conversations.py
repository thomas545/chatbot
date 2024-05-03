from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    EnumField,
)
from databases.mongo_dbs import Databases, Collections
from .resources import Resource
from core.constants import TicketStatus, TicketPriority


class Ticket(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.TICKETS,
    }

    user_id = StringField(db_field="user_id", required=True)
    ticket_ref = StringField(db_field="ticket_ref")

    subject = StringField(db_field="subject")
    description = StringField(db_field="description")
    created_by = StringField(db_field="created_by", required=True)
    assigned_to = StringField(db_field="assigned_to", required=False)
    status = EnumField(
        db_field="status",
        enum=TicketStatus,
        required=True,
        default=TicketStatus.OPEN,
    )
    priority = EnumField(
        db_field="priority",
        enum=TicketPriority,
        required=True,
        default=TicketPriority.LOW,
    )
    is_active = BooleanField(default=True)
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)


class Conversation(Document):
    meta = {
        "db_alias": Databases.MAIN_DB,
        "collection": Collections.CONVERSATIONS,
    }

    user_id = StringField(db_field="user_id", required=True)
    resource_id = ReferenceField(Resource, db_field="resource_id", required=False)
    ticket_id = ReferenceField(Ticket, db_field="ticket_id", required=False)
    query = StringField(db_field="query")
    response = StringField(db_field="response")
    created_at = DateTimeField(db_field="created_at", default=datetime.utcnow)
    updated_at = DateTimeField(db_field="updated_at", default=datetime.utcnow)
