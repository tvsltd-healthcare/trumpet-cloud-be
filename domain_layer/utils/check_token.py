from domain_layer.abstractions.request_interface import IRequest
from domain_layer.auth_manager import AuthManager


def check_bearer_token(request: IRequest) -> bool | dict:
    authorization = request.get_headers().get('authorization')
    if not authorization or not authorization.startswith("Bearer "):
        return False
    token = authorization.split("Bearer ")[1]

    auth_getter_adapter = AuthManager.get()
    check_token = auth_getter_adapter.validate_token(token)
    if check_token:
        read_token_data = auth_getter_adapter.read_data(token)
        return read_token_data
    else:
        return False



