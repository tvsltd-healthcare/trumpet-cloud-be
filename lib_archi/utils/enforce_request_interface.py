from lib_archi.abstractions.request_interface import IRequest

from functools import wraps


def enforce_request_type():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if not isinstance(request, IRequest):
                raise TypeError(
                    f"'request' must conform to IRequest, Make sure {type(request).__name__} signatures matches with IRequest"
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator