from core.environment import get_environ


class Databases:
    MAIN_DB = get_environ("MONGO_MAIN_DB_NAME")


class Collections:
    RESOURCES = "resources"
    CONVERSATIONS = "conversations"
