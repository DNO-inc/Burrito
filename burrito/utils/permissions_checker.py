from functools import wraps


def check_permission(func):
    """_summary_

    Args:
        func (_type_): wrapper
    """

    @wraps(func)
    async def wrap(*args, **kwargs):
#        print(args, kwargs)
        return await func(*args, **kwargs)

    return wrap
