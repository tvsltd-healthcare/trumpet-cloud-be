from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Updates the status of a study agreement for the requesting user's organization.
    If all associated organization agreements are approved, the overall study agreement
    is marked as approved.

    Workflow:
    1. Extracts and validates required request data.
    2. Verifies that the study agreement and the organization-specific agreement exist.
    3. Updates the organization's agreement status.
    4. If all org agreements for the study are approved, marks the overall study agreement as approved.

    Args:
        request (IRequest): Request object containing JSON body, headers, and context.

    Returns:
        dict: A formatted response from ResponseFormatter with either:
            - success: containing updated organization agreement info
            - error: with appropriate HTTP status and message
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
