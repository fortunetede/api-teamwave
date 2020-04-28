from django.core.cache import cache

def set_cache(key, value):
    cache.set(key, value, timeout=None)
    print("Cache just got set with key: %s"%(key))
    pass

def get_cache(key):
    print("Cache just got called with key: %s"%(key))
    return cache.get(key)