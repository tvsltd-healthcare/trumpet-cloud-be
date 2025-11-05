import requests

from starlette import status

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    response_formatter = ResponseFormatter()

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    organizations_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Organizations")
    organization_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")

    organization = get_current_user_org(request, organizations_repo, organization_users_repo)

    don_host_url = organization.get("host")

    print("don_host_url", don_host_url)

    try:
        response = requests.get(f"{don_host_url}/ping", timeout=5)
        if response.status_code != 200:
            return response_formatter.error(message="Failed to connect to Data Owner Node.", status_code=status.HTTP_400_BAD_REQUEST)

        print("response", response)
    except Exception as e:
        print(e)
        return response_formatter.error(message="Failed to connect to Data Owner Node.", status_code=status.HTTP_400_BAD_REQUEST)

    return response_formatter.success(message="Successfully connect to Data Owner Node.", status_code=status.HTTP_200_OK, data=None)


def get_current_user_org(request: IRequest, organizations_repo: IAppRepoInvoker, organization_users_repo: IAppRepoInvoker):
    auth_header = request.get_headers().get("authorization")
    if not auth_header:
        raise Exception("No authorization header provided.")

    decoded_token = token_parser(auth_header)

    user_id = decoded_token.get("user_id")

    print({"user_id": user_id})

    organization_users = organization_users_repo.get(query={"user_id": user_id}, is_collection=False)

    organization_id =  organization_users.get("organization_id")

    organization = organizations_repo.get(query={"id": organization_id}, is_collection=False)

    print("organization", organization)

    return organization
