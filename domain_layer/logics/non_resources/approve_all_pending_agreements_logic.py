from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    response_formatter = ResponseFormatter()

    current_user_role = get_current_user_role(request)
    if current_user_role != 'trumpet_admin':
        return response_formatter.error(message="Not allowed", status_code=401)

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    study_agreements_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("StudyAgreements")
    organization_study_agreements_repo = repo_getter.get_repo_invoker("OrganizationStudyAgreements")

    pending_study_agreements = study_agreements_repo.get({"status": "pending"}, is_collection=True)

    for pending_study_agreement in pending_study_agreements:
        study_agreement_id = pending_study_agreement.get("id")

        study_agreements_repo.transact("PATCH", data={"status": "approved"}, query={'id': study_agreement_id})
        organization_study_agreements_repo.transact("PATCH", data={"status": "approved"}, query={"study_agreement_id": study_agreement_id})

    return response_formatter.success(message="Organization study agreement status updated successfully.",
                                      data={"pending_study_agreement": pending_study_agreements},
                                      status_code=201)


def get_current_user_role(request: IRequest):
    auth_header = request.get_headers().get("authorization")
    if not auth_header:
        raise Exception("No authorization header provided.")

    decoded_token = token_parser(auth_header)

    user_id = decoded_token.get("user_id")

    return get_user_role(user_id)


def get_user_role(user_id: int):
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    user_roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("UserRoles")
    user_role = user_roles_repo.get({"user_id": user_id}, is_collection=False)

    roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Roles")
    role = roles_repo.get({"id": user_role.get("role_id")}, is_collection=False)

    return role.get('name')
