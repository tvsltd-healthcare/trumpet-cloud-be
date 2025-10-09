import time
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser
from domain_layer.websocket_pool_manager import WebsocketPoolManager

RESEARCHER_ADMIN = "researcher_admin"
DATA_OWNER_ADMIN = "data_owner_admin"
APPROVED_STATUS = "approved"


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    response_formatter: IResponseFormatter = ResponseFormatter()

    current_user_id = _authorize_and_get_user_id(request)
    if not current_user_id:
        return response_formatter.error("Authenticated user ID not found in token.", 401)

    id_dict = request.get_path_params()
    org = repo.get(id_dict)

    if not org:
        return response_formatter.error("Organization not found.", 404)

    org_status = org['status']

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Organizations")
    organization = organization_repo_invoker.get({"host": entity.host}, False)
    if organization and organization.get('id') != org['id']:
        errors = [{
            "field": "host",
            "message": "Organization with this host already exists.",
            "error_code": "101"
        }]
        return response_formatter.validation_error(message="Organization with this host already exists.", status_code=409, errors=errors)

    updated_org = repo.patch(entity, id_dict)
    updated_org_status = updated_org['status']

    if updated_org_status == APPROVED_STATUS and updated_org_status != org_status:
        admin_user_ids = _admin_user_ids_for_org(org['id'])
        _notify_user_channels(admin_user_ids, current_user_id)

    return response_formatter.success(updated_org, 'Information successfully updated.', 200)


def _authorize_and_get_user_id(request: IRequest):
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    return decoded_token.get('user_id')


def _admin_user_ids_for_org(org_id):
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    organization_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")
    organization_users = organization_users_repo.get({"organization_id": org_id}, is_collection=True)
    user_ids = [item["user_id"] for item in organization_users]

    roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Roles")
    roles = roles_repo.get({"name": [RESEARCHER_ADMIN, DATA_OWNER_ADMIN]}, is_collection=True)
    role_ids = [item["id"] for item in roles]

    user_roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("UserRoles")
    user_roles = user_roles_repo.get({"user_id": user_ids, "role_id": role_ids}, is_collection=True)
    admin_user_ids = [item["user_id"] for item in user_roles]

    return admin_user_ids


def _notify_user_channels(receiver_user_ids, current_user_id):
    websocket_pool = WebsocketPoolManager.get()

    for receiver_user_id in receiver_user_ids:
        websocket_notification: dict = {'type': 'organization_approved', 'created_at': time.time() * 1000, }

        websocket_pool.broadcast_json(f'users/{receiver_user_id}', websocket_notification)
        _save_notification_to_db(websocket_notification, receiver_user_id, current_user_id)


def _save_notification_to_db(websocket_notification, receiver_user_id, current_user_id):
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    notification_dict = websocket_notification.copy()
    notification_dict.pop("created_at", None)
    notification_dict['user_id'] = receiver_user_id
    notification_dict['message'] = "Your organization has been approved!"
    notification_dict['created_by'] = current_user_id
    notification_dict['updated_by'] = current_user_id

    notifications_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Notifications")
    notifications_repo.transact("POST", data=notification_dict)
