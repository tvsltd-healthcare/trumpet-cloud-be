from fastapi import HTTPException
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser

@enforce_request_type()
def execute(request: IRequest):
    # todo: auth: LGTM. VALUR FROM TOKEN

    try:
        response_formatter = ResponseFormatter()

        auth_header = request.get_headers().get('authorization')
        decoded_token = token_parser(auth_header)
        organization_id = decoded_token.get('organization_id', None)

        if not organization_id:
            return response_formatter.error('Token must provide organization id', 400)
        
        body = request.get_json()

        repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

        dataset_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Datasets")
        dataset = dataset_repo.get({"don_uid": body['don_uid'], "organization_id": organization_id}, is_collection=False)

        if not dataset:
            return response_formatter.error("Dataset could not be found!", 404)
        
        try:
            dataset_repo.transact( "PATCH", data={'status': 'unpublished'}, query={'id': dataset.get('id')})
        except Exception as e:
            return ResponseFormatter().error(str(e), 500)
        
        return response_formatter.success( {}, 'Successfully Unpublished!', 200)

    except Exception as e:
        return response_formatter.error(str(e), 500)
