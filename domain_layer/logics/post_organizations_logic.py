from domain_layer.utils.parse_token import token_parser
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager

@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Handles the creation of organizations by validating the request and entity, 
    extracting user information from the authorization token, and invoking the repository's post method.

    Args:
        request (IRequest): An object implementing the request interface, 
                            expected to contain headers and path parameters.
        repo: The repository instance responsible for handling persistence logic.
        entity (optional): The entity to be persisted. Must have an `email` attribute.

    Returns:
        dict: A formatted response dictionary, either success or error, using the ResponseFormatter.
              - Success: Contains the created organization data and HTTP 201 status.
              - Error: Contains an error message and appropriate HTTP status (e.g., 400 or 500).

    Raises:
        Exception: Any unexpected exceptions raised during repository operation will be caught 
                   and returned as a 500 error response.

    Notes:
        - Requires a valid "Authorization" header with a Bearer token.
        - Token must decode to include an "email" field.
        - The entity will be enriched with the email from the token before saving.
    """
    response_formatter: IResponseFormatter = ResponseFormatter()

    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Users")

    # Validate entity
    if entity is None:
        return response_formatter.error('Entity cannot be None', 400)

    # Remove "Bearer " prefix from token and decode data
    decode_token = token_parser(request.get_headers()['authorization'])
    email = decode_token.get("email")
    type = decode_token.get("organization_type")
    
    if not email or not type:
        return response_formatter.error('Email or Organization Type Missing.', 400)
    
    entity.email = email
    entity.type = type

    if repo.get({'email': entity.email}):
        return response_formatter.error('Organization with this email already exists.', 409)

    if repo.get({'phone': entity.phone}):
        return response_formatter.error('Organization with this phone number already exists.', 409)

    if user_repo.get({'phone': entity.phone}):
        return response_formatter.error('User with this phone number already exists.', 409)


    try:
        create_organizations = repo.post(entity, request.get_path_params())
        
        if create_organizations:
            return response_formatter.success( create_organizations, 'Organizations created successfully.', 201 )
        else:
            return response_formatter.error('Organizations created failed', 500)

    except Exception as e:
        return response_formatter.error(str(e), 500)
