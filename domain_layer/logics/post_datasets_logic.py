from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser

def execute(request: IRequest, repo, entity=None):
    """
    Creates a new dataset and associates it with an organization based on the organization ID found in the JWT token.

    Workflow:
    1. Extracts the Authorization token from the request headers.
    2. Decodes the token to retrieve the organization ID.
    3. Attaches the organization ID to the dataset entity.
    4. Creates the dataset using the provided repository.
    5. Returns the newly created dataset data with a success response.

    Args:
        request (IRequest): An object containing headers and parameters, including the Authorization token.
        repo (Any): A repository object responsible for creating the dataset (must implement `post`).
        entity (Optional[Dict[str, Any]]): The dataset data to be created. Must not be None.

    Returns:
        Dict[str, Any]: A formatted success or error response containing dataset data or failure reason.

    Raises:
        ValueError: If the token is missing or the organization ID cannot be determined.
        Exception: For any unexpected errors during processing.
    """
    
    response_formatter = ResponseFormatter()

    if entity is None:
        return response_formatter.error('Entity cannot be None', 400)

    try:
        auth_header = request.get_headers().get('authorization')
        decoded_token = token_parser(auth_header)
        organization_id = decoded_token.get('organization_id', None)

        if not organization_id:
            return response_formatter.error('Token must provide organization id', 400)
        
        body = request.get_json()
        dataset = repo.get({"don_uid": body['don_uid'], "organization_id": organization_id})

        if dataset:
            pass
            # uncommet this block after adding status to datasets
            # try:
            #     dataset_status_update = repo.transact( "PATCH", data={'status': 'published'}, query={'id': dataset.get('id')})
            # except Exception as e:
            #     return ResponseFormatter().error(str(e), 500)
        else:
            entity.organization_id = organization_id
            dataset = repo.post(entity, ids={})
        
        return response_formatter.success(dataset, 'Dataset created successfully.', 201)
    except Exception as e:
        return response_formatter.error(str(e), 500)
