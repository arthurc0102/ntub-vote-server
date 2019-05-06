from functools import wraps


def short_description(name):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner.short_description = name
        return inner
    return decorator
