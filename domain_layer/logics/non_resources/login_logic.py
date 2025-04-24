from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.auth_manager import AuthManager
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter

@enforce_request_type()
def execute(request: IRequest):
    body = request.get_json()
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    query = {
        "email": body.get("email"),
    }
    user = user_repo_invoker.get(query, False)
    response: IResponseFormatter = ResponseFormatter()
    if user:
        # check password
        password_handler = PasswordManager.get()
        check_password = password_handler.verify_password(body.get('password'), user.get('password'))
        if check_password:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token({"user_id": user.get('id')})
            return response.success(data=token, message="User successfully logged in.", status_code=200)
        else:
            return response.error(message="Invalid password.", status_code=404)
    else:
        return response.error(message="User not found", status_code=404)
