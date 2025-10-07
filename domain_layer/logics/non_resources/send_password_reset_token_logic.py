from domain_layer.auth_manager import AuthManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

@enforce_request_type()
def execute(request: IRequest):

    """
    Handles the "forgot password" flow by generating a reset token and sending it via email to the user.

    Workflow:
    1. Extracts the user's email from the request body.
    2. Looks up the user in the "Users" repository using the provided email.
    3. If the user exists:
        - Generates a password reset token.
        - Sends a verification email with the reset token.
        - Returns a success response.
    4. If the user does not exist, returns an error response.

    Parameters:
        request (IRequest): A request object conforming to the IRequest interface.
            Expected JSON body format:
                {
                    "email": "user@example.com"
                }

    Returns:
        dict: A formatted JSON-compatible dictionary response with:
            - 200 status code if the email was sent successfully.
            - 500 status code if the user does not exist or if any exception occurs.

    Raises:
        Does not raise exceptions directly; all errors are caught and returned via the response formatter.

    Note:
        - The function depends on various domain-layer managers (AuthManager, EmailServiceManager, etc.).
        - The token is generated with a flag `reset_password: True` for downstream validation.
    """

    body = request.get_json()
    email = body.get("email")
    query = { "email": email }

    response_formatter = ResponseFormatter()
    # discovery repo
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    user = user_repo.get(query, False)

    if user:
        auth_getter_adapter = AuthManager.get()
        token = auth_getter_adapter.generate_token({ "email": email, "reset_password": True})
        token_value = token["token"] if isinstance(token, dict) else token

        email_service = EmailServiceManager.get()
        #Should be backgroud task
        try:
            email_service.send_email(email, token_value, type='reset_password')
        except Exception as e:
            return response_formatter.error(str(e), 500)

        return response_formatter.success( {}, 'Email has been sent successfully.', 200)
    else:
        return response_formatter.error('User does not exists', 404)



