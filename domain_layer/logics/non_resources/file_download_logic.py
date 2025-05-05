from starlette.responses import FileResponse

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type


@enforce_request_type()
def execute(request: IRequest):
    body = request.get_query_params()
    file_id = body.get('file_id')
    response_formatter = ResponseFormatter()

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

    try:
        file = files_repo.get({'id': file_id})
        if not file:
            response_formatter.error('File missing.', 400)

        # TO-DO: HardCoded directory path needs to change.
        file_path = "/Users/tvs/projects/tvs-enterprise/trumpet_be_cloud_platform/" + file.get('path')

        return FileResponse(file_path)  # type: ignore

    except Exception as e:
        print('Error:::', e)
        return response_formatter.error(str(e), 500)
