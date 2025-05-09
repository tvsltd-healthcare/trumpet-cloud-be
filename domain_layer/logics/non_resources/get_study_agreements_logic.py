import json

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Retrieves all study agreements associated with the current user's organization,
    filtered by optional status or other query parameters.

    Steps:
    1. Identify the current user's organization using the token.
    2. Parse and validate optional query filters (e.g., status).
    3. Fetch organization-study-agreements for the user's org.
    4. Fetch and return corresponding study agreements if any.

    Args:
        request (IRequest): The incoming request containing headers and optional query parameters.

    Returns:
        dict: Formatted response with a list of matched study agreements, or error details.
    """
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    try:
        # Step 1: Get the current user's organization ID
        org_id = _get_current_user_org_id(request, repo_discovery_service)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)

        # Step 2: Parse query filters (e.g., filter={"status": "approved"})
        query_filter = _parse_query_filter(request)

        # Step 3: Fetch org-study-agreements for the current organization
        org_agreements = _get_org_study_agreements(
            repo_discovery_service,
            organization_id=org_id,
            filters=query_filter
        )
        if not org_agreements:
            return response_formatter.error("No organization study agreements found.", 404)

        study_agreement_ids = [
            item.get("study_agreement_id")
            for item in org_agreements
            if item.get("study_agreement_id") is not None
        ]

        if study_agreement_ids:
            # Step 5: Fetch study agreements if IDs exist
            study_agreement_repo = repo_discovery_service.get_repo_invoker("StudyAgreements")
            study_agreements = study_agreement_repo.get(
                {'id': study_agreement_ids},
                is_collection=True
            )
        else:
            study_agreements = []

        study_agreements = [_add_org_approval_to_study_agreement(study_agreement, org_agreements)
                            for study_agreement in study_agreements]

        return response_formatter.success(
            study_agreements,
            message="Study agreements retrieved successfully.",
            status_code=200
        )

    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using the JWT token in the Authorization header."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None


def _parse_query_filter(request: IRequest) -> dict:
    """Safely parses the 'filter' query parameter into a dictionary."""
    query_params = request.get_query_params()
    raw_filter = query_params.get('filter', {}) if isinstance(query_params, dict) else {}

    try:
        _filter = json.loads(raw_filter) if isinstance(raw_filter, str) else raw_filter
        if _filter.get('org_approval_status') is not None:
            _filter['status'] = _filter.get('org_approval_status')

        _filter.pop('org_approval_status', None)

        return _filter
    except (json.JSONDecodeError, TypeError):
        return {}


def _get_org_study_agreements(
        repo_discovery_service: IAppRepoDiscoveryGetter,
        organization_id: int,
        filters: dict
) -> list[dict]:
    """Fetches organization-study-agreement records for a given organization, applying optional filters."""
    org_agreement_repo = repo_discovery_service.get_repo_invoker("OrganizationStudyAgreements")
    query = {"organization_id": organization_id, **filters}
    return org_agreement_repo.get(query, is_collection=True)


def _add_org_approval_to_study_agreement(study_agreement, org_agreements):
    for org_agreement in org_agreements:
        if study_agreement.get("id") == org_agreement.get("study_agreement_id"):
            study_agreement["org_approval_status"] = org_agreement.get("status")
    return study_agreement
