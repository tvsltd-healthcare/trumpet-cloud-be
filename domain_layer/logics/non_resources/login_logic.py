import time

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.auth_manager import AuthManager
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter


@enforce_request_type()
def execute(request: IRequest):
    body = request.get_json()
    response_formatter: IResponseFormatter = ResponseFormatter()

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Users")

    email = body.get("email")
    if not email:
        return response_formatter.error(message="Email is required.", status_code=400)
    email = email.lower().strip()

    password = body.get("password")
    if not password:
        return response_formatter.error(message="Password is required.", status_code=400)


    user = user_repo.get({"email": email}, False)
    if user is None:
        return response_formatter.error(message="Invalid username or password. Please try again!", status_code=404)
    # todo: sign-up user with the same deleted email. need to add in future
    if user["status"] == "deleted":
        return response_formatter.error(message="Invalid username or password. Please try again!", status_code=404)

    if not user:
        return response_formatter.error(message="Invalid username or password. Please try again!", status_code=404)

    if not _is_valid_password(body.get("password"), user.get("password")):
        return response_formatter.error(message="Invalid username or password. Please try again!", status_code=404)

    token = _generate_token(user["id"])
    if not token:
        return response_formatter.error(message="Login failed.", status_code=404)

    role_name = _get_user_role_name(repo_getter, user["id"])
    if not role_name:
        return response_formatter.error(message="Login failed.", status_code=404)

    organization = _get_user_organization_name(repo_getter, user["id"])
    if not organization:
        return response_formatter.error(message="Login failed.", status_code=404)

    return response_formatter.success(data=_build_success_response(token, user, role_name, organization),
        message="Login successful.", status_code=200)


def _is_valid_password(raw_password: str, hashed_password: str) -> bool:
    password_manager = PasswordManager.get()
    return password_manager.verify_password(raw_password, hashed_password)


def _generate_token(user_id: str) -> dict | None:
    auth_manager = AuthManager.get()
    return auth_manager.generate_token({"user_id": user_id})


def _get_user_role_name(repo_getter: IAppRepoDiscoveryGetter, user_id: str) -> str | None:
    role_user_repo = repo_getter.get_repo_invoker("UserRoles")
    role_user = role_user_repo.get({"user_id": user_id}, False)
    if not role_user:
        return None

    role_repo = repo_getter.get_repo_invoker("Roles")
    role = role_repo.get({"id": role_user["role_id"]}, False)
    if not role:
        return None

    return role["name"]


def _get_user_organization_name(repo_getter: IAppRepoDiscoveryGetter, user_id: str) -> dict | None:
    organization_user_repo = repo_getter.get_repo_invoker("OrganizationUsers")
    organization_user = organization_user_repo.get({"user_id": user_id}, False)
    if not organization_user:
        return None

    organization_repo = repo_getter.get_repo_invoker("Organizations")
    organization = organization_repo.get({"id": organization_user["organization_id"]}, False)
    if not organization:
        return None

    return {
        "id": organization.get("id", None),
        "name": organization.get("name", None),
        "type": organization.get("type", None),
        "status": organization.get("status", None),
    }


def _build_success_response(token: dict, user: dict, role_name: str, organization: str) -> dict:
    return {
        "access_token": token["token"],
        "expires_in": int(time.time()) + int(token["expires"]),
        "user": {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone_number": user["phone"],
            "status": user["status"],
            "role": role_name,
            "organization": organization,
        }
    }
