def paginate_queryset(queryset, page=1, limit=10):
    offset = int((page - 1) * limit)
    total_count = queryset.count()
    queryset = queryset.skip(offset).limit(limit)
    return queryset, total_count
