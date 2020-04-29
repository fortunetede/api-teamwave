from django.core.cache import cache
from django.core.paginator import Paginator
import datetime, time

def set_cache(key, value):
    cache.set(key, value, timeout=None)
    print("Cache just got set with key: %s"%(key))
    pass

def get_cache(key):
    print("Cache just got called with key: %s"%(key))
    return cache.get(key)

def custom_paginator(myqueryset, pagesize, client_page_pagination):
    paginated_questions = Paginator(myqueryset, 5)
    page_results = paginated_questions.page(int(client_page_pagination))
    print("page_results", page_results)
    # previous and next
    previous = int(client_page_pagination) - 1
    if previous <= 0:
        previous = None
    _next = int(client_page_pagination) + 1
    if _next * int(client_page_pagination) > int(pagesize):
        _next = None
    final_result = {
        "Previous": previous,
        "Next": _next,
        "Current": int(client_page_pagination),
        "Count": paginated_questions.count,
        "status": "01",
        "results": page_results.object_list
    }
    return final_result

def date_to_seconds(_date):
    strdate = str(_date)
    year = strdate[:4]
    month = strdate[5:7]
    day = strdate[8:]
    t = datetime.datetime(int(year), int(month), int(day), 0, 0)
    seconds = str(time.mktime(t.timetuple()))[:-2]
    return int(seconds)