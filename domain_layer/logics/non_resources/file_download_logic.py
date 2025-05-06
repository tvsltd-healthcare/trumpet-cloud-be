from starlette.responses import FileResponse
from pathlib import Path
import os
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type

OUTPUT_DIR = os.getenv('FILE_UPLOAD_ABS_DIR')

@enforce_request_type()
def execute(request: IRequest):
    body = request.get_json()
    file_id = body.get('file_id')
    response_formatter = ResponseFormatter()

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

    try:
        file = files_repo.get({'id': file_id})
        if not file:
            response_formatter.error('File missing.', 400)

        file_path = Path(OUTPUT_DIR).absolute() / file.get('filename')

        return FileResponse(file_path)  # type: ignore

    except Exception as e:
        print('Error:::', e)
        return response_formatter.error(str(e), 500)
