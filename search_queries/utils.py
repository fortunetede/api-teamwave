from django.core.cache import cache
from django.core.paginator import Paginator

def set_cache(key, value):
    cache.set(key, value, timeout=None)
    print("Cache just got set with key: %s"%(key))
    pass

def get_cache(key):
    print("Cache just got called with key: %s"%(key))
    return cache.get(key)

def custom_paginator(myqueryset, pagesize, page):
    paginated_questions = Paginator(myqueryset, 5)
    page_results = paginated_questions.page(page)
    # previous and next
    previous = int(page) - 1
    if previous <= 0:
        previous = None
    _next = int(page) + 1
    if _next * int(page) > int(pagesize):
        _next = None
    final_result = {
        "Previous": previous,
        "Next": _next,
        "Current": int(page),
        "Count": paginated_questions.count,
        "status": "01",
        "results": page_results.object_list
    }
    return final_result