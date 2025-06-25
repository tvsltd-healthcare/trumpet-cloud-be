import json
import re

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.get_users import get_users


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Logic to get a notification by its ID and enrich it with user information.
    :param request: IRequest object containing the request data.
    :param repo: Repository object to interact with the database.
    :param entity: Optional entity type, not used in this logic.
    :return: ResponseFormatter object with the enriched notification data.
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
