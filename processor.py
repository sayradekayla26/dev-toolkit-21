import collections
import functools
import itertools

def deep_flatten(items):
    """Recursively flatten nested iterables with a generator."""
    for x in items:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, (str, bytes)):
            yield from deep_flatten(x)
        else:
            yield x

def memoize_with_expiry(ttl=60):
    """Decorator for caching results with a simple timestamp check."""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache and (now - cache[args]['time'] < ttl):
                return cache[args]['val']
            result = func(*args)
            cache[args] = {'val': result, 'time': now}
            return result
        return wrapper
    return decorator

def batch_process(data, size):
    """Partition data into chunks using itertools recipes."""
    it = iter(data)
    return iter(lambda: tuple(itertools.islice(it, size)), ())

def pipeline(data, *funcs):
    """Functional pipe pattern execution over data."""
    return functools.reduce(lambda d, f: f(d), funcs, data)

if __name__ == '__main__':
    data = [1, [2, 3], [[4], 5]]
    print(list(deep_flatten(data)))