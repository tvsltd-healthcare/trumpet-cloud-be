from fastapi import HTTPException
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest):
    """
    Handles the "forgot password" or invitation flow by checking if a user exists.
    If the user does not exist, generates a token and sends it via email.

    This method:
    1. Retrieves the email from the request body.
    2. Checks if a user already exists with the given email.
    3. If not, generates a token and sends an email using the configured email service.
    4. If the user already exists, returns an error indicating duplication.

    Args:
        request (IRequest): An object implementing the IRequest interface containing the JSON body.

    Returns:
        dict: A formatted response from ResponseFormatter.
              - Success: Indicates the email has been sent with a 200 status code.
              - Error: If the user already exists or email sending fails, returns a 500 error.

    Raises:
        Exception: Any issues during email generation or sending are caught and returned as 500 error.

    Example:
        ```python
        request = Request(json={"email": "john@example.com"})
        result = execute(request)
        # If user doesn't exist: {"status": "success", "message": "Successfully email send.", "data": {}}
        # If user exists: {"status": "error", "message": "User already registered with this email.", ...}
        ```
    """
    response_formatter = ResponseFormatter()

    body = request.get_json()

    email = body.get("email")
    if not email:
        return response_formatter.error('Email field is required.', 400)
    email = email.strip().lower()

    organization_type = body.get("organization_type")
    if not organization_type:
        return response_formatter.error('Organization type field is required.', 400)

    if organization_type not in ["data_owner", "researcher"]:
        return response_formatter.error('Invalid organization type.', 400)

    query = { "email": email }

    role = "data_owner_admin" if organization_type == "data_owner" else "researcher_admin"

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    try:
        user = user_repo_invoker.get(query, False)

        if not user:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token({
                "email": email, "role": role, "organization_type": organization_type})

            token_value = token["token"] if isinstance(token, dict) else token

            email_service = EmailServiceManager.get()
            email_service.send_email(email, token_value, type='varify_org')
            return response_formatter.success( {}, 'Successfully email send.', 200)
        else:
            return response_formatter.error('Organization already registered with this email.', 400)

    except Exception as e:
        return response_formatter.error(str(e), 500)


