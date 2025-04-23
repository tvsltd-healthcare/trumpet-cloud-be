from functools import wraps

from domain_layer.abstractions.request_interface import IRequest


def enforce_request_type():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not isinstance(request, IRequest):
                raise TypeError(
                    f"'request' must conform to IRequest, Make sure {type(request).__name__} signatures matches with IRequest"
                )
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
