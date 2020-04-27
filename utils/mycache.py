import memcache

cache = memcache.Client(['47.93.151.99:11211'],debug=True)


def set(key,value,timeout=300):
    # 添加其他代码
    return cache.set(key,value,timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)