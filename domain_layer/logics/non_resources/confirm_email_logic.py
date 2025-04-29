from domain_layer.auth_manager import AuthManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter


def execute(request):
    """
    Verifies a user token, checks if the user not exists by email, and generates a new token if not.
    
    Args:
        request: The request object containing a JSON body with a token.
    
    Returns:
        Dict containing message, status_code, and optional data.
    """

    body = request.get_json()
    auth_getter_adapter = AuthManager.get()
    response_formatter = ResponseFormatter()

    decode_token = auth_getter_adapter.read_data(body.get("token"))
    email = decode_token.get("email")
    if not email:
        return response_formatter.error('Email missing.',400)

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    try:
        user = user_repo_invoker.get({"email": email}, False)
        if not user:
            auth_getter_adapter = AuthManager.get()
            # TODO: If not assgin user_id then when we create user then token is not valid in auth middleware
            # Adding user_id = 1 temporary
            token = auth_getter_adapter.generate_token({"email": email, "user_id": 1}) 
            if token:
                return response_formatter.success( token, 'User token verify successfully.', 200)
            else:
                return response_formatter.error('Failed to generate new token.',400)
        else:
            return response_formatter.error('User already exits',403)

    except Exception as e:
        return response_formatter.error(str(e), 500)
