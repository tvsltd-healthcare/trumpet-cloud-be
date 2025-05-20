from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Executes a request to retrieve and format a study agreement entity with related organization
    agreement details.

    Handles the retrieval of the current user's organization details, queries organization
    study agreements using specific filters, and incorporates the organization agreement status
    into the study agreement entity before returning a formatted response.

    Args:
        request (IRequest): The request object containing details such as path parameters
            and user context.
        repo: A repository instance used to fetch the study agreement entity.
        entity (optional): An additional entity that might be used during execution.

    Raises:
        ValueError: If the user is not assigned to any organization.
        KeyError: If the required path parameters are missing or incorrect.

    Returns:
        A formatted response object containing the retrieved entity and its associated
        organization agreement status, or an error message in case of failure.
    """
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    org_id = _get_current_user_org_id(request, repo_discovery_service)
    if not org_id:
        return response_formatter.error("User is not assigned to any organization.", 403)

    ids = request.get_path_params()

    query_filter = {
        "study_agreement_id": int(ids.get("id"))
    }

    org_agreements = _get_org_study_agreements(
        repo_discovery_service,
        organization_id=org_id,
        filters=query_filter
    )

    if not org_agreements:
        return response_formatter.error("No organization study agreements found.", 404)

    study_agreement = repo.get(ids=ids)

    study_agreement["org_approval_status"] = org_agreements.get("status")

    # get participants info
    if study_agreement.get("participants") is not None:
        split_participants = study_agreement.get("participants").split(",")
        users_list = []
        for participant in split_participants:
            users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Users")
            users = users_repo.get({"id": participant})
            if users:
                user_info = {
                    "id": users.get("id"),
                    "first_name": users.get("first_name"),
                    "last_name": users.get("last_name"),
                    "email": users.get("email"),
                    "status": users.get("status"),
                    "phone": users.get("phone"),
                }
                users_list.append(user_info)

        study_agreement["participant_users"] = users_list

    return response_formatter.success(
        data=study_agreement,
        message="Entity retrieved successfully",
        status_code=200
    )


def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using the JWT token in the Authorization header."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None


def _get_org_study_agreements(
        repo_discovery_service: IAppRepoDiscoveryGetter,
        organization_id: int,
        filters: dict
) -> object | None | list[object]:
    """Fetches organization-study-agreement records for a given organization, applying optional filters."""
    org_agreement_repo = repo_discovery_service.get_repo_invoker("OrganizationStudyAgreements")
    query = {"organization_id": organization_id, **filters}
    return org_agreement_repo.get(query, is_collection=False)
