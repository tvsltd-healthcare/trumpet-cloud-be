from lib_archi.abstractions.request_interface import IRequest

from functools import wraps


def enforce_request_type():
    """Decorator to enforce that the first argument to a function is an IRequest instance.

        This ensures that logic functions using the IRequest abstraction are passed
        a compatible request object, promoting type safety and decoupling from framework-specific implementations.

        Returns:
            Callable: A decorated function that checks the type of the `request` argument.

        Raises:
            TypeError: If the `request` argument does not implement the IRequest interface.
        """
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
