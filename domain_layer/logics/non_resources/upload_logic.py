import anyio
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

def execute(request):
    
    try:
        body = anyio.from_thread.run(request.form)
        auth_header = request.headers['authorization']

        # Remove "Bearer " prefix
        token = auth_header.replace("Bearer ", "").strip()
        
        file = body.get("file")
        if file is None:
            return {"message": "No file provided", "status_code": 400}

        auth_getter_adapter = AuthManager.get()
        decode_token = auth_getter_adapter.read_data(token)

        repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        files_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Files")

        create_files_body = {
            "filename": file.filename,
            "type": body.get("type"),
            "buffer": body.get("buffer"),
            "path":  f"{body.get('resource_name')}:{decode_token['user_id']}:{file.filename}",
            "size": file.size,
            "mime_type": file.headers.get('content-type'),
            "owner": f"{body.get('resource_name')}:{decode_token['user_id']}",
        }
        
        print('create_files_body=========>>>',create_files_body)
        # create_file = files_repo_invoker.transact("POST", data =create_files_body)

        return {
            "message": "File created successfully.",
            # "data": create_file,
            "status_code": 200,
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": str(e), "status_code": 500}