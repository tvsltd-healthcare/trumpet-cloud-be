from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Updates the status of a study agreement for the requesting user's organization.
    If all associated organization agreements are approved, the overall study agreement
    is marked as approved.

    Workflow:
    1. Extracts and validates required request data.
    2. Verifies that the study agreement and the organization-specific agreement exist.
    3. Updates the organization's agreement status.
    4. If all org agreements for the study are approved, marks the overall study agreement as approved.

    Args:
        request (IRequest): Request object containing JSON body, headers, and context.

    Returns:
        dict: A formatted response from ResponseFormatter with either:
            - success: containing updated organization agreement info
            - error: with appropriate HTTP status and message
    """
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    try:
        # Step 1: Get current user's organization ID
        org_id = _get_current_user_org_id(request, repo_discovery_service)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)

        # Step 2: Parse and validate request body
        body = request.get_json()
        study_agreement_id = body.get('study_agreement_id')
        status = body.get('status')

        if not study_agreement_id or not status:
            return response_formatter.error("Both 'study_agreement_id' and 'status' are required.", 400)

        # Step 3: Verify study agreement exists
        study_agreement_repo = repo_discovery_service.get_repo_invoker("StudyAgreements")
        study_agreement = study_agreement_repo.get({'id': study_agreement_id})
        if not study_agreement:
            return response_formatter.error("Study agreement not found.", 404)

        # Step 4: Get and update org-specific agreement
        org_agreement_repo = repo_discovery_service.get_repo_invoker("OrganizationStudyAgreements")
        org_agreement_query = {
            'study_agreement_id': study_agreement_id,
            'organization_id': org_id
        }

        org_agreement = org_agreement_repo.get(org_agreement_query)
        if not org_agreement:
            return response_formatter.error("Study agreement not found for this organization.", 404)

        updated_org_agreement = org_agreement_repo.transact(
            "PATCH",
            data={'status': status},
            query=org_agreement_query
        )

        # Step 5: Check if all org agreements are approved
        all_do_org_agreements = org_agreement_repo.get(
            {'study_agreement_id': study_agreement_id, 'organization_type': 'data_owner'},
            is_collection=True
        )

        if _are_all_org_agreements_approved(all_do_org_agreements):
            org_agreement_repo.transact(
                "PATCH",
                data={'status': 'approved'},
                query={'study_agreement_id': study_agreement_id, 'organization_type': 'researcher'}
            )
            
            study_agreement_repo.transact(
                "PATCH",
                data={'status': 'approved'},
                query={'id': study_agreement_id}
            )

        return response_formatter.success(
            updated_org_agreement,
            message="Organization study agreement status updated successfully.",
            status_code=200
        )

    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using their token."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None


def _are_all_org_agreements_approved(agreements: list[dict]) -> bool:
    """Returns True if all organization agreements have status 'approved'."""
    return all(item.get("status") == "approved" for item in agreements)
