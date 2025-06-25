import time
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.websocket_pool_manager import WebsocketPoolManager


RESEARCHER_ADMIN = "researcher_admin"
DATA_OWNER_ADMIN = "data_owner_admin"
APPROVED_STATUS = "approved"

@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    response_formatter: IResponseFormatter = ResponseFormatter()

    id_dict = request.get_path_params()
    org = repo.get(id_dict)
    
    if not org:
        return response_formatter.error("Organization not found.", 404)
    
    org_status = org['status']

    updated_org = repo.patch(entity, id_dict)
    updated_org_status = updated_org['status']

    if updated_org_status == APPROVED_STATUS and updated_org_status != org_status:
        admin_user_ids = _admin_user_ids_for_org(org['id'])
        _notify_user_chanels(admin_user_ids)

    return response_formatter.success( updated_org, 'Entity updated successfully', 200 )


def _admin_user_ids_for_org(org_id):
    print('org_id', org_id)
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    organization_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")
    organization_users = organization_users_repo.get({"organization_id": org_id}, is_collection=True)
    user_ids = [item["user_id"] for item in organization_users]
    print('user_ids', user_ids)

    roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Roles")
    roles = roles_repo.get({"name": [RESEARCHER_ADMIN, DATA_OWNER_ADMIN]}, is_collection=True)
    role_ids = [item["id"] for item in roles]
    print('role_ids', role_ids)

    user_roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("UserRoles")
    user_roles = user_roles_repo.get({"user_id": user_ids, "role_id": role_ids}, is_collection=True)
    admin_user_ids = [item["user_id"] for item in user_roles]
    print('admin_user_ids', admin_user_ids)

    return admin_user_ids


def _notify_user_chanels(user_ids):
    websocket_pool = WebsocketPoolManager.get()

    for user_id in user_ids:
        websocket_pool.broadcast_json(f'users/{user_id}', {
            'type': 'organization_approved',
            'created_at': time.time() * 1000,
        })
