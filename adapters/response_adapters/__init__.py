from adapters.response_adapters.response_handler import ResponseHandler
from application_layer.abstractions.response_interface import IResponseHandler


def get_response_handler() -> IResponseHandler:
    """
    Factory function that returns an instance of the ResponseHandler implementing IResponseHandler.
    """
    return ResponseHandler()
