import json
import re

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.get_role import get_role_name
from domain_layer.utils.parse_token import token_parser
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.response_formatter import ResponseFormatter


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
      Executes the main application workflow to process a given request by interacting
      with the provided repository and optionally an entity. The process involves extracting
      path and query parameters, parsing them safely, fetching related records from the
      repository, and subsequently interacting with an additional "Files" repository to
      enrich the records with file details.

      Args:
          request (IRequest): The request object containing path and query parameters.
          repo: The primary repository interface used for querying data.
          entity (optional): Additional entity context for execution.

      Returns:
          Dict: A formatted response containing the retrieved data or an error message.
      """
    response_formatter = ResponseFormatter()

    try:
        ids = request.get_path_params()
    except KeyError:
        return response_formatter.error(
            message="Path parameters are missing in the request.",
            status_code=400
        )

    try:
        int(ids.get("id"))
    except ValueError:
        return response_formatter.error(
            message=f"Invalid dataset ID",
            status_code=400
        )

    dataset = repo.get(ids)
    if not dataset:
        return response_formatter.error(
            message="Dataset not found.",
            status_code=404
        )

    _add_org_details_to_items([dataset])
    _parse_json_attrs([dataset])

    return response_formatter.success(
        dataset,
        message="Dataset retrieved successfully.",
        status_code=200
    )

def _add_org_details_to_items(collected_records: dict):
    unique_org_ids = {item["organization_id"] for item in collected_records if item["organization_id"] is not None}
    unique_org_ids = list(unique_org_ids)

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Organizations")

    orgs = organization_repo.get({'id': unique_org_ids}, is_collection=True)

    org_dict = { org["id"]: org for org in orgs }

    for record in collected_records:
        org_id = record.get("organization_id")
        record["organization_details"] = org_dict.get(org_id)


def _parse_json_attrs(collected_records):
    for record in collected_records:
        record["statistics"] = json.loads(record["statistics"])
