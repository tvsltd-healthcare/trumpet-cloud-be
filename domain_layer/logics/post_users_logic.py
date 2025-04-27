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

    try:
        # Validate entity
        if entity is None:
            raise ValueError("Entity cannot be None")
        
        # Remove "Bearer " prefix from token and decode data
        decode_token = token_parser(request.get_headers()['authorization'])
        email = decode_token.get("email")
        if not email:
            raise ValueError("Email not found in token")
        
        # Make password hash
        password_handler = PasswordManager.get()
        entity.password = password_handler.hash_password(getattr(entity, 'password', None))
        entity.email = email

        create_user = repo.post(entity, request.get_path_params())
        if not create_user:
            raise RuntimeError("User creation failed: Invalid or empty response from users")
        
        # Manage repositary
        repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        organization_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Organizations")
        organization_users_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("OrganizationUsers")

        get_organization_by_email = organization_repo.get({ "email": email })
        if not get_organization_by_email:
            raise RuntimeError("Organization retrieval failed: Invalid or empty response from organizations")
        
        # Assgin user to organization based on token
        organization_users = {
            "user_id": create_user.get("id"),
            "organization_id": get_organization_by_email.get("id")
        }
        user_assign_to_organization = organization_users_repo.transact("POST", data =organization_users)
        if not user_assign_to_organization:
            raise RuntimeError("Failed to assign user to organization: Invalid response from organization users")

        return create_user

    except ValueError as ve:
        raise ValueError(f"Validation error: {str(ve)}")
    except KeyError as ke:
        raise KeyError(f"Missing required key: {str(ke)}")
    except AttributeError as ae:
        raise AttributeError(f"Invalid attribute access: {str(ae)}")
    except RuntimeError as re:
        raise RuntimeError(f"Operation failed: {str(re)}")
    except Exception as e:
        raise ValueError(f"Token parsing failed: {str(e)}")
    
