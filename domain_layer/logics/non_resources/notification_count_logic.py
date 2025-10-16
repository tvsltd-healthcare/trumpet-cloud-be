from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Retrieves the count of unread notifications for the currently authenticated user.
    This function performs the following steps:
        1. Parses the authorization token from the request headers.
        2. Extracts the user ID from the decoded token.
        3. Uses the Notifications repository to count unread notifications for that user.
        4. Returns a success response with the count of unread notifications.
    Args:
        request (IRequest): The request object containing headers with authorization token.
    Returns:
        ResponseFormatter: A formatted response containing the count of unread notifications.
    """
    # todo: auth: LGTM. done via token data.

    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    try:

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

