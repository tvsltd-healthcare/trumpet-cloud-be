from domain_layer.utils.token_parser import token_parser
from domain_layer.utils.file_upload import upload_file_to_disk
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

def create_files_body(form_data, upload_file, decode_token):
    return {
            "filename": upload_file.get("file_name"),
            "type": form_data.get("type"),
            "buffer": form_data.get("buffer"),
            "path":  f"{upload_file.get("file_path")}",
            "size": upload_file.get("file_size"),
            "mime_type": upload_file.get("file_mime_type"),
            "owner": f"{form_data.get('resource_name')}:{decode_token.get("user_id")}"
        }

@enforce_request_type()
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
        form_data = request.get_form_data()
        file = form_data.get("file")
        upload_file = upload_file_to_disk(file)

        # Remove "Bearer " prefix from token and decode data
        decode_token = token_parser(request.get_headers()['authorization'])

        # Manage repositary
        repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

        file_body = create_files_body(form_data, upload_file, decode_token)
        create_file = files_repo.transact("POST", data = file_body)
        return {
            "message": "File created successfully.",
            "data": create_file,
            "status_code": 200
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": str(e), "status_code": 500}