from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser

def execute(request: IRequest, repo, entity=None):
    """
    Creates a new user, assigns them to an organization based on the token's email, and returns the user data with the organization ID.

    This method:
    1. Change password string to hash and then create a user using the provided entity and query parameters.
    2. Decodes the JWT token from the Authorization header to get the email.
    3. Retrieves the organization by email using the Organizations repository.
    4. Assigns the user to the organization via the OrganizationUsers repository.
    5. Adds the organization ID to the user data.

    Args:
        request (IRequest): Request object with headers (Authorization token) and query parameters.
        repo (Any): Repository object for creating users (must have a `post` method).
        entity (Optional[Dict[str, Any]]): User data to create. Defaults to None.

    Returns:
        Dict[str, Any]: Created user data with `organization_id` added.

    Raises:
        ValueError: If Authorization header, token email, or required IDs are missing/invalid.
        KeyError: If required keys (e.g., `id`, `organization_id`) are missing in repository responses.
        AttributeError: If entity or required methods are missing/invalid.
        RuntimeError: If repository operations (post, get, transact) fail or return invalid data.

    Example:
        ```python
        request = Request(headers={'authorization': 'Bearer <token>'}, query_params={})
        repo = UserRepository()
        entity = {'first_name': 'John', 'email': 'john@example.com'}
        result = execute(request, repo, entity)
        # Returns: {'id': 54, 'first_name': 'John', ..., 'organization_id': 123}
        ```
    """
    response_formatter = ResponseFormatter()

    # Validate entity
    if entity is None:
        return response_formatter.error('Entity cannot be None', 400)

    # Remove "Bearer " prefix from token and decode data

    try:
        print(f"{entity}")
        # api_token = request.get_headers()['authorization']

        auth_header = request.get_headers().get('authorization')
        decoded_token = token_parser(auth_header)
        print(f"{decoded_token}")

        organization_id = decoded_token.get('organization_id')
        entity.organization_id = organization_id
        saved_entity = repo.post(entity, ids={})

        print(f"{saved_entity=}")

        return response_formatter.success(entity, 'Dataset created successfully.', 201)

    except Exception as e:
        return response_formatter.error(str(e), 500)
