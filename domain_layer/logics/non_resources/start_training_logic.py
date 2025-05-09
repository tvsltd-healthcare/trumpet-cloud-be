import json
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser
from logic_injector.base_logic_injector import BaseLogicInjector


def execute(request: IRequest):
    """
    Validates and prepares a study agreement operation for the current user's organization.

    Validation Steps:
    1. Verifies that the current user belongs to a researcher-type organization.
    2. Accepts optional filter parameters and retrieves the matching organization study agreements.
    3. Ensures the associated study agreement is in 'approved' status.
    4. Verifies that all linked data owner organizations have a non-null 'host' field.

    Args:
        request (IRequest): Incoming request with headers and optional query parameters.

    Returns:
        dict: A formatted success response if all validations pass, or an error response.
    """
    response_formatter = ResponseFormatter()
    repo_discovery: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    try:
        # Step 1: Check if study agreement exists in db and is in approved state
        body = request.get_json()
        study_agreement_id = body.get('study_agreement_id')
        
        if not study_agreement_id:
            return response_formatter.error("Study agreement not found.", 403)
        
        study_agreement_repo = repo_discovery.get_repo_invoker("StudyAgreements")
        study_agreement = study_agreement_repo.get({"id": study_agreement_id})
        
        if not study_agreement:
            return response_formatter.error("Study Agreement not found.", 403)
        
        study_agreement_status = study_agreement.get('status', None)

        if study_agreement_status != 'approved':
            return response_formatter.error("Study Agreement is not approved.", 403)
        
        # Step 2: Resolve current user's organization
        org_id = _get_current_user_org_id(request, repo_discovery)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)

        org_repo = repo_discovery.get_repo_invoker("Organizations")
        organization = org_repo.get({"id": org_id})
        if not organization or organization.get("type") != "researcher":
            return response_formatter.error("Not Permitted.", 403)

        # Step 3: Check if agreement has at least one data owner
        org_agreement_repo = repo_discovery.get_repo_invoker("OrganizationStudyAgreements")
        do_org_agreements = org_agreement_repo.get(
            {"study_agreement_id": study_agreement_id, 'organization_type': 'data_owner'},
            is_collection=True
        )

        if not do_org_agreements:
            return response_formatter.error("No data owner organization found study agreements found.", 404)
        
        # Step 4: Retrive and sort data owner hosts saved in Organizations table as host list
        do_org_ids = [
            a.get("organization_id") for a in do_org_agreements if a.get("organization_id")
        ]

        org_repo = repo_discovery.get_repo_invoker("Organizations")

        data_owner_orgs = org_repo.get({"id": do_org_ids, "type": "data_owner"}, is_collection=True)

        sorted_do_orgs = sorted(data_owner_orgs, key=lambda x: x.get("id", 0))
        host_list = [org.get("host") for org in sorted_do_orgs]

        # step 5: Start Training
        injector = BaseLogicInjector()
        ids = { 'study_id': study_agreement.get('study_id') }
        agreement_id = study_agreement.get('id')
        injector.inject_business_logic(entity=study_agreement, entity_id=ids, agreement_id=agreement_id, host_list=host_list)
        
        return response_formatter.success(
            message="Traning Started Successfully.",
            data=study_agreement,
            status_code=202
        )
    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using the Authorization token."""
    auth_header = request.get_headers().get("authorization")
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get("user_id")

    org_users_repo = repo_discovery.get_repo_invoker("OrganizationUsers")
    org_user = org_users_repo.get({"user_id": current_user_id})

    return org_user.get("organization_id") if org_user else None
