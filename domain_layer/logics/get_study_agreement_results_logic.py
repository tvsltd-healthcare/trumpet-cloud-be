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
from domain_layer.utils.get_users import get_users


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

    ids = request.get_path_params()
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    study_agreement_results_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("StudyAgreementResults")

    # Extract organization_id
    study_agreement_results = study_agreement_results_repo.get({"study_agreement_id": ids.get('study_agreement_id'), "id": ids.get("id")}, False)
    if not study_agreement_results:
        return response_formatter.error('Study Agreement Result not found', 400)

    user_ids = []
    if study_agreement_results.get("created_by") is not None:
        user_ids.append(study_agreement_results.get("created_by"))

    if study_agreement_results.get("updated_by") is not None:
        user_ids.append(study_agreement_results.get("updated_by"))

    if user_ids is not None and len(user_ids) > 0:
        user_info = get_users(repo_discovery_getter, user_ids)
        if user_info:
            for user in user_info:
                user_data = {
                    "id": user.get("id"),
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "email": user.get("email"),
                    "phone": user.get("phone")
                }
                if user.get("id") == study_agreement_results.get("created_by"):
                    study_agreement_results["created_by"] = user_data
                if user.get("id") == study_agreement_results.get("updated_by"):
                    study_agreement_results["updated_by"] = user_data
    return response_formatter.success(
        data=study_agreement_results,
        message="Study Agreement Result retrieved successfully.",
        status_code=200
    )

