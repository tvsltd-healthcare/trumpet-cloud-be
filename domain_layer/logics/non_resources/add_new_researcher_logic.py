from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    password_handler = PasswordManager.get()

    body = request.get_json()

    decode_token = token_parser(request.get_headers()['authorization'])

    email = decode_token.get("email")
    if not email:
        return response_formatter.error('Email missing.', 400)

    organization_id = decode_token.get("organization_id")
    if organization_id is None:
        return response_formatter.error('Organization missing.', 400)

    role_name = "researcher"

    try:
        user = {
            "first_name": body.get("first_name"),
            "last_name": body.get("last_name"),
            'email': email,
            'phone': body.get("phone"),
            'password': password_handler.hash_password(body.get("password")),
        }
        user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Users")
        created_user = user_repo.transact("POST", data=user)
        if not created_user:
            return response_formatter.error('User creation failed: Invalid or empty response from users.', 500)
        created_user.pop("password", None)

        organization_users = {
            "user_id": created_user.get("id"),
            "organization_id": organization_id
        }
        organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
        user_assign_to_organization = organization_users_repo.transact("POST", data=organization_users)
        if not user_assign_to_organization:
            return response_formatter.error(
                'Failed to assign user to organization: Invalid response from organization user', 500)

        role_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Roles")
        role = role_repo.get({"name": role_name})
        if not role:
            return response_formatter.error('Role retrieval failed: Invalid or empty response from roles', 500)

        role_user = {
            "user_id": created_user.get("id"),
            "role_id": role.get("id")
        }
        role_user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("UserRoles")
        role_user_repo.transact("POST", data=role_user)
        if not created_user:
            return response_formatter.error('User creation failed: Invalid or empty response from users.', 500)

        return response_formatter.success(created_user, 'User created successfully.', 201)

    except Exception as e:
        return response_formatter.error(str(e), 500)
