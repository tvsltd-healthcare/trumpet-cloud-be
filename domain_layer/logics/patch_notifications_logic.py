from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.get_users import get_users
from datetime import datetime


def execute(request: IRequest, repo, entity=None):
    """
    Logic to patch a notification by its ID and mark it as read.
    This function retrieves a notification by its ID, marks it as read if it is not already,
    and enriches it with user information for the creator, updater, and target user.
    It returns the updated notification data along with user details.
    This function performs the following steps:
      1. Extracts the notification ID from the request path parameters.
      2. Retrieves the notification from the repository.
      3. Checks if the notification is already marked as read.
      4. If not read, updates the notification to mark it as read and sets the read timestamp.
      5. Collects user IDs associated with the notification (creator, updater, target user).
      6. Fetches user details for these IDs and enriches the notification data with this information.
      7. Returns a success response with the updated notification data.
    Args:
        request (IRequest): The request object containing path parameters.
        repo: The repository interface used to interact with the notification data.
        entity (Any, optional): Currently unused, present for interface consistency.

    Returns:
        ResponseFormatter: A formatted response containing the updated notification data.
    """

    response_formatter = ResponseFormatter()
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    # Step 1: Extract path and query params
    id = request.get_path_params()

    collected_records = repo.get(id)

    check_status = collected_records.get("is_read")
    if not check_status:
        notification = {
            'is_read': True,
            'read_at': datetime.now()
        }
        updated_repo_data = repo.patch(notification, id)
        collected_records = updated_repo_data
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
    return response_formatter.success(collected_records, message="Notification updated successfully.", status_code=200)
