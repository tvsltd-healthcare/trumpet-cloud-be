from domain_layer.password_manager import PasswordManager
from domain_layer.utils.parse_token import token_parser
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter


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
        RuntimeError: If repository operations (post, get, transact) fail.

    Example:
        ```python
        request = Request(headers={'authorization': 'Bearer <token>'}, query_params={})
        repo = UserRepository()
        entity = {'first_name': 'John', 'email': 'john@example.com'}
        result = execute(request, repo, entity)
        # Returns: {'id': 54, 'first_name': 'John', ..., 'organization_id': 123}
        ```
    """

    try:
        # Make password hash
        password_handler = PasswordManager.get()
        entity.password = password_handler.hash_password(getattr(entity, 'password', None))

        create_user = repo.post(entity, request.get_query_params())
        
        # Remove "Bearer " prefix from token and decode data
        decode_token = token_parser(request.get_headers()['authorization'])
        if not decode_token["email"]:
            raise ValueError("Email not found in token.")

        # Manage repositary
        repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        organization_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Organizations")
        organization_users_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("OrganizationUsers") 
        get_organization_by_email = organization_repo_invoker.get({"email":decode_token['email']})
    
        # Assgin user to organization based on token
        organization_users = {
            "user_id": create_user.get("id"),
            "organization_id": get_organization_by_email.get("id")
        }
        user_assign_to_organization = organization_users_repo_invoker.transact("POST", data =organization_users)

        return {**create_user, "organization_id": user_assign_to_organization["organization_id"]}
    except Exception as e:
        raise RuntimeError(f"User creation failed: {str(e)}")
