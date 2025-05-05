from django.core.cache import cache

def manage_incr() -> int:
    '''
        Will increment the integer
        stored in cache. If not created, it will insert it first.
    '''
    val = cache.get('id')
    if not val:
        cache.set('id', '0')
        return 0
    else:
        cache.set('id', str(int(val) + 1))
        return val
    