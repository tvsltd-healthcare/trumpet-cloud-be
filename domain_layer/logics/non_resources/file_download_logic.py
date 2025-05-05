from domain_layer import response_formatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.token_parser import token_parser
from domain_layer.utils.file_upload import upload_file_to_disk
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from fastapi import FastAPI, Response # type: ignore


@enforce_request_type()
def execute(request: IRequest):
    body = request.get_json()
    file_id = body.get('file_id')
    response_formatter = ResponseFormatter()

    # Manage repositary
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

    try:
        file = files_repo.get({'id': file_id})
        if not file:
             response_formatter.error('File missing.', 400)

        file_path = file.get('path')


        return FileResponse(file_path) # type: ignore
        # with open(file_path, 'r') as file:
        #     content = file.read()
        #     print('content', content)
        # return response_formatter.success( 'data', 'User token verify successfully.', 200)




    except Exception as e:
        print('Error:::',e)
        return response_formatter.error(str(e), 500)
