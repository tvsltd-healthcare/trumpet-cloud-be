import anyio
from domain_layer.auth_manager import AuthManager
from domain_layer.utils.file_upload import upload_file_to_disk
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter


def execute(request):
    """
    Handles file upload, authentication, and metadata creation for a file resource.

    Steps:
    1. Extracts form data from the incoming request.
    2. Uploads the file to disk.
    3. Extracts and decodes the JWT token from the Authorization header.
    4. Retrieves the appropriate file repository invoker.
    5. Constructs a file metadata dictionary and prepares it for storage or further processing.

    Args:
        request: The incoming HTTP request object containing form data and headers.

    Returns:
        dict: A JSON-serializable dictionary containing a success or error message,
              status code, and file metadata if successful.
    """
    
    try:
        body = body = anyio.from_thread.run(lambda: request.form())

        file = body.get("file")
        upload_file = upload_file_to_disk(file)

        # Remove "Bearer " prefix from token and decode data
        auth_header = request.headers['authorization']
        token = auth_header.replace("Bearer ", "").strip()
        auth_getter_adapter = AuthManager.get()
        decode_token = auth_getter_adapter.read_data(token)

        # Manage repositary
        repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        files_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Files")

        create_files_body = {
            "filename": upload_file['file_name'],
            "type": body.get("type"),
            "buffer": body.get("buffer"),
            "path":  f"{body.get('resource_name')}:{decode_token['user_id']}:{upload_file['file_name']}",
            "size": file.size,
            "mime_type": file.headers.get('content-type'),
            "owner": f"{body.get('resource_name')}:{decode_token['user_id']}",
        }
        
        print('create_files_body=========>>>',create_files_body)
        # create_file = files_repo_invoker.transact("POST", data =create_files_body)

        return {
            "message": "File created successfully.",
            "data": create_files_body,
            "status_code": 200,
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": str(e), "status_code": 500}