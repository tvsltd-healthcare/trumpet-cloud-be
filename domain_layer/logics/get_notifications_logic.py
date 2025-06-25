from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.get_users import get_users


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Retrieves a notification by its ID and enriches it with user information.
    This function performs the following steps:
      1. Extracts the notification ID from the request path parameters.
      2. Retrieves the notification from the repository.
      3. Collects user IDs associated with the notification (creator, updater, target user).
      4. Fetches user details for these IDs and enriches the notification data with this information.
      5. Returns a success response with the updated notification data.
    Args:
        request (IRequest): The request object containing path parameters.
        repo: The repository interface used to interact with the notification data.
        entity (Any, optional): Currently unused, present for interface consistency.
    Returns:
        ResponseFormatter: A formatted response containing the notification data enriched with user details.
    """
    response_formatter = ResponseFormatter()
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    # Step 1: Extract path and query params
    id = request.get_path_params()

    collected_records = repo.get(id)
    user_ids = []
    if collected_records.get("created_by") is not None:
        user_ids.append(collected_records.get("created_by"))

    if collected_records.get("updated_by") is not None:
        user_ids.append(collected_records.get("updated_by"))

    if collected_records.get("user_id") is not None:
        user_ids.append(collected_records.get("user_id"))

    if user_ids and len(user_ids) > 0:
        user_info = get_users(repo_discovery_getter, user_ids)
        if user_info:
            for user in user_info:
                user_data = {
                    "id": user.get("id"),
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "email": user.get("email"),
                    "phone": user.get("phone")
                }
                if user.get("id") == collected_records.get("created_by"):
                    collected_records["created_by_user"] = user_data
                if user.get("id") == collected_records.get("updated_by"):
                    collected_records["updated_by_user"] = user_data
                if user.get("id") == collected_records.get("user_id"):
                    collected_records["target_user"] = user_data
    return response_formatter.success(collected_records, message="Notification retrieved successfully.", status_code=200)
