import time

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.authorization_manager import AuthorizationManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.utils.authorization import get_user_id, is_supper_admin
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser
from domain_layer.websocket_pool_manager import WebsocketPoolManager


APPROVED_STATUS = "approved"

@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    response_formatter: IResponseFormatter = ResponseFormatter()

    current_user_id = _authorize_and_get_user_id(request)
    if not current_user_id:
        return response_formatter.error("Authenticated user ID not found in token.", 401)

    id_dict = request.get_path_params()

    user_id = id_dict.get("id")


    if not check_permission(request, user_id):
        return response_formatter.error("Not allowed.", 403)

    user = repo.get(id_dict)
    if not user:
        return response_formatter.error("User not found.", 404)

    if repo.get({'phone': entity.phone}):
        return response_formatter.error("This phone number is already in use. Please enter a different number.", 409)

    user_status = user['status']

    updated_user = repo.patch(entity, id_dict)
    updated_user_status = updated_user['status']

    if updated_user_status == APPROVED_STATUS and updated_user_status != user_status:
        _notify_user_channel(user['id'], current_user_id)

    return response_formatter.success( updated_user, 'Information successfully updated.', 200 )


def _authorize_and_get_user_id(request: IRequest):
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    return decoded_token.get('user_id')


def _notify_user_channel(receiver_user_id, current_user_id):
    websocket_pool = WebsocketPoolManager.get()

    websocket_notification: dict = {
        'type': 'user_approved',
        'created_at': time.time() * 1000,
    }

    websocket_pool.broadcast_json(f'users/{receiver_user_id}', websocket_notification)
    _save_notification_to_db(websocket_notification, receiver_user_id, current_user_id)


def _save_notification_to_db(websocket_notification, receiver_user_id, current_user_id):
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    notification_dict = websocket_notification.copy()
    notification_dict.pop("created_at", None)
    notification_dict['user_id'] = receiver_user_id
    notification_dict['message'] = "You have been approved!"
    notification_dict['created_by'] = current_user_id
    notification_dict['updated_by'] = current_user_id

    notificatoins_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Notifications")
    notificatoins_repo.transact("POST", data=notification_dict)


def check_permission(request: IRequest, user_id: int):
    current_user_id = get_user_id(request)

    if is_supper_admin(current_user_id):
        return True

    authorization_handler: IFGAAuthorizer = AuthorizationManager.get()

    permision = authorization_handler.check({
            "user_type": "user",
            "user_id": current_user_id,
            "action": "update",
            "resource_type": "user",
            "resource_id": user_id,
        })

    return permision.get('allowed')