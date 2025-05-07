from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest, repo, entity=None):
    """
    Creates a new study and assigns it to the user's organization based on the token's user ID.

    This method:
    1. Decodes the JWT token from the Authorization header to extract the user ID.
    2. Retrieves the user's organization from the OrganizationUsers repository.
    3. Assigns the organization_id to the study entity.
    4. Creates the study using the provided repository and path parameters.
    5. Returns the created study data with a success message.

    Args:
        request (IRequest): Request object containing headers (Authorization token) and query/path parameters.
        repo (Any): Repository object for creating studies (must have a `post` method).
        entity (Optional[Dict[str, Any]]): Study data to create (e.g., name, description). Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - The created study data (e.g., id, name, description, organization_id).
            - A success message and HTTP status code (201) on successful creation.
            - An error message and appropriate HTTP status code (400, 500) on failure.

    Raises:
        ValueError: If the Authorization header is missing or the token is invalid.
        KeyError: If the token lacks a user_id or required keys are missing in repository responses.
        AttributeError: If the entity is None or lacks required attributes for study creation.
        RuntimeError: If repository operations (get, post) fail or return invalid data.
    """

    decode_token = token_parser(request.get_headers()['authorization'])
    response_formatter = ResponseFormatter()

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_users_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("OrganizationUsers")

    try:
        organization_user = organization_users_repo.get({"user_id": decode_token.get('user_id')}, False)
        organization_id = organization_user.get('organization_id')
        if not organization_id:
            return response_formatter.error('Organization not found', 400)

        entity.organization_id = organization_id
        create_study = repo.post(entity, request.get_path_params())

        if create_study:
            return response_formatter.success( create_study, 'Study created successfully.', 201 )
        else:
            return response_formatter.error('Study created failed', 500)

    except Exception as e:
        return response_formatter.error(str(e), 500)
