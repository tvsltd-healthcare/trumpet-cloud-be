import json

from datetime import datetime, timedelta, timezone

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser
from logic_injector.base_logic_injector import BaseLogicInjector

def execute(request: IRequest):
    try:
        response_formatter = ResponseFormatter()

        repo_discovery: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        dataset_repo = repo_discovery.get_repo_invoker("Datasets")
        org_repo = repo_discovery.get_repo_invoker("Organizations")
        study_agreement_repo = repo_discovery.get_repo_invoker("StudyAgreements")
        org_agreement_repo = repo_discovery.get_repo_invoker("OrganizationStudyAgreements")
        org_users_repo = repo_discovery.get_repo_invoker("OrganizationUsers")

        body = request.get_json()
        study_agreement_id = body.get('study_agreement_id')
        
        if not study_agreement_id:
            return response_formatter.error("Study agreement not found.", 403)
        
        study_agreement = study_agreement_repo.get({"id": study_agreement_id}, is_collection=False)

        if not study_agreement:
            return response_formatter.error("Study Agreement not found.", 403)

        study_agreement['pet_config'] = json.loads(study_agreement['pet_config'])
        
        study_agreement_status = study_agreement.get('status', None)

        if study_agreement_status != 'approved':
            return response_formatter.error("Study Agreement is not approved.", 403)

        org_id = _get_current_user_org_id(request, org_users_repo)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)
        
        organization = org_repo.get({"id": org_id}, is_collection=False)
        if not organization or organization.get("type") != "researcher":
            return response_formatter.error("Not Permitted.", 403)
        
        do_org_agreements = org_agreement_repo.get(
            {"study_agreement_id": study_agreement_id, 'organization_type': 'data_owner'},
            is_collection=True
        )

        do_study_agreement_and_dataset = [
            {
                "organization": get_organization(do_org_agreement, org_repo),
                "dataset": get_dataset(do_org_agreement, dataset_repo)
            }
            for do_org_agreement in do_org_agreements
        ]

        BaseLogicInjector().inject_business_logic(study_agreement=study_agreement, do_org_agreements=do_study_agreement_and_dataset)

        next_training_time = datetime.now(timezone.utc) + timedelta(minutes=5)

        study_agreement_repo.transact(
            method="PATCH",
            data={"next_training_time": next_training_time},
            query={"id": study_agreement_id}
        )

        return response_formatter.success(
            message="Training Started Successfully.",
            data=study_agreement,
            status_code=202
        )
    except Exception as e:
        return response_formatter.error(f"Internal server error.", 500)

def _get_current_user_org_id(request: IRequest, org_users_repo) -> int | None:
    """Extracts the current user's organization ID using the Authorization token."""
    auth_header = request.get_headers().get("authorization")
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get("user_id")

    org_user = org_users_repo.get({"user_id": current_user_id}, is_collection=False)

    return org_user.get("organization_id") if org_user else None


def get_organization(do_org_agreement, org_repo):
    organization = org_repo.get({"id": do_org_agreement["organization_id"], "type": "data_owner"}, is_collection=False)
    return organization

def get_dataset(do_org_agreement, dataset_repo):
    dataset = dataset_repo.get({"id": do_org_agreement["dataset_id"]}, is_collection=False)
    return dataset