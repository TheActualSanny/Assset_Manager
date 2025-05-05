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
    
def formatted_title(file_name: str) -> str:
    '''
        In managaer classes' methods where we
        do lookups for certain assets, this method will be
        called to compare the actual names instead of blob names.
    '''
    return file_name.split('_')[1]

