from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Retrieves the count of unread notifications for the current user.
    This function performs the following steps:
        1. Parses the Authorization header to extract the current user's ID.
        2. Retrieves the organization ID associated with the current user.
        3. Queries the Notifications repository for unread notifications.
        4. Returns the count of unread notifications in a formatted response.
    Args:
        request (IRequest): The request object containing headers and parameters.
    Returns:
        ResponseFormatter: A formatted response containing the unread notification count or an error message.
    """

    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    try:
        # Step 1: Get current user's organization ID
        org_id = _get_current_user_org_id(request, repo_discovery_service, current_user_id)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)

        notification_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Notifications")
        notifications_results = notification_repo.get({"is_read": False, "user_id": current_user_id}, True)
        notification_count = len(notifications_results)
        return response_formatter.success(
            data={
                "unread_notification_count": notification_count
            },
            message="Notification count retrieved successfully.",
            status_code=200
        )

    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter, current_user_id) -> int | None:
    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None
