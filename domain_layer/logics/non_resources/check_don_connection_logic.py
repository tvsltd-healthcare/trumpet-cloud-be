import os

import requests
from starlette import status

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser

FL_AGG_TOKEN = os.getenv("FL_AGG_TOKEN")


def execute(request: IRequest):
    response_formatter = ResponseFormatter()

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    print("Decoded Token:", decoded_token)

    body = request.get_json()
    organization_id = body.get("organization_id")
    if not organization_id:
        return response_formatter.error(message="Organization ID is required.", status_code=status.HTTP_400_BAD_REQUEST)

    organizations_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Organizations")

    organization = organizations_repo.get(query={"id": organization_id}, is_collection=False)

    print(organization)

    don_host_url = organization.get("host")

    print("don_host_url", don_host_url)

    try:
        response = requests.get(f"{don_host_url}/ping", timeout=5)

        is_don_accessible = True

        if response.status_code == 200:
            message = "Successfully connect to Data Owner Node Backend."
        else:
            message = "Failed to connect to Data Owner Node Backend.",
            is_don_accessible = False

        response = requests.get(f"{don_host_url}:8081/health", timeout=5,
                                headers={"Authorization": f'Bearer {FL_AGG_TOKEN}'})

        if response.status_code == 200:
            message += "\nSuccessfully connect to FL Core DO."
        else:
            message += "\nFailed to connect to FL Core DO."
            is_don_accessible = False

        if is_don_accessible:
            return response_formatter.success(message=message, status_code=status.HTTP_200_OK, data=None)
        else:
            return response_formatter.error(message=message, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Failed to connect to Data Owner Node.")
        print(e)
        return response_formatter.error(message="Failed to connect to Data Owner Node.",
                                        status_code=status.HTTP_404_NOT_FOUND)
