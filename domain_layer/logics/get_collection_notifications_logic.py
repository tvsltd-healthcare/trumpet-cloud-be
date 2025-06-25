from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Retrieves a collection of notifications for the currently authenticated user.
    This function performs the following steps:
      1. Extracts the user ID from the request state.
      2. Uses the Notifications repository to fetch notifications for that user.
      3. Returns a success response with the retrieved notifications.
    Args:
        request (IRequest): The request object containing user context.
        repo: Not used in this context, present for interface consistency.
        entity (Any, optional): Not used in this context, present for interface consistency.
    Returns:
        ResponseFormatter: A formatted response containing the notifications data.
    """
    response_formatter = ResponseFormatter()

    # Step 1: Extract path and query params
    user_id = request.get_request().scope.get('state').get('user_id')

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    notifications_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Notifications")

    notifications = notifications_repo.get({"user_id": user_id}, True)

    return response_formatter.success(
        notifications,
        message="Data retrieved successfully.",
        status_code=200
    )
