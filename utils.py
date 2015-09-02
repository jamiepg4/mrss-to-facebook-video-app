import functools


def memoize(obj):
    """
    Wrap a function with memoization.

    Parameters:
        obj: a callable object (e.g. a function).

    Returns:
        A decorator that memoizes values returned by the function it decorates.
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
