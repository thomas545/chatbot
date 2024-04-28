from mongoengine import (
    StringField,
    IntField,
    ListField,
    EnumField,
    BooleanField,
    FloatField,
)


def get_field_type(document_class, attr):

    field = getattr(document_class, attr)
    mapping = {
        StringField: str,
        IntField: int,
        ListField: list,
        EnumField: str,
        BooleanField: bool,
        FloatField: float,
    }
    return mapping[type(field)]


def get_sort_value(sort_key, sort_order):
    if sort_key and isinstance(sort_key, str):
        if sort_order == "desc":
            sort_key = f"-{sort_key}"
    return sort_key


def filter_queryset(
    queryset,
    query_params,
    search_fields=None,
    filter_fields=None,
    ordering_fields=None,
):
    filter_query = {}
    search_query = {"$or": []}
    search = query_params.get("searchValue", "")
    sort_key = query_params.get("sortKey")
    sort_order = query_params.get("sortOrder")

    if search_fields and search:
        for search_key in search_fields:
            search_query["$or"].append(
                {search_key: {"$regex": search, "$options": "i"}}
            )

    if not search_query.get("$or", []):
        search_query = {}

    if filter_fields:
        for field in filter_fields:
            if field in query_params:
                field_type = get_field_type(queryset._document, field)
                value = query_params.get(field)
                regex = "$in" if (("," in value) or field_type is list) else "$eq"
                if value:
                    if "," in value:
                        value = value.split(",")
                    elif field_type is list:
                        value = [value]
                    elif field_type is bool:
                        value = bool(int(value))
                    elif field_type is float:
                        value = float(value)

                    filter_query[field] = {regex: value}

    ordering = get_sort_value(sort_key, sort_order)

    queryset = (
        queryset.filter(__raw__=search_query)
        .filter(__raw__=filter_query)
        .order_by(ordering)
    )
    if not ordering and ordering_fields:
        order_keys = []
        for ordering_field, order in ordering_fields:
            order_query = get_sort_value(ordering_field, order)
            order_keys.append(order_query)
        queryset = queryset.order_by(*order_keys)
    return queryset
