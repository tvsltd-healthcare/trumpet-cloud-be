from domain_layer.utils.token_parser import token_parser
from domain_layer.utils.file_upload import upload_file_to_disk
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter


def create_files_body(form_data, upload_file, organization_user):
    return {
        "filename": upload_file.get("file_name"),
        "type": form_data.get("type"),
        "path": f"{upload_file.get('file_path')}",
        "size": upload_file.get("file_size"),
        "mime_type": upload_file.get("file_mime_type"),
        "organization_id": organization_user.get("organization_id"),
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
    response_formatter = ResponseFormatter()
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    # Remove "Bearer " prefix from token and decode data
    decode_token = token_parser(request.get_headers()['authorization'])
    print(f"{decode_token=}")

    user_id = decode_token.get("user_id")

    if not user_id:
        return response_formatter.error('Invalid token: user_id missing.', 400)

    organization_user_repo = repo_discovery_getter.get_repo_invoker("OrganizationUsers")
    organization_user = organization_user_repo.get({"user_id": user_id}, False)
    if not organization_user:
        return response_formatter.error('Invalid token: user_id not found.', 400)

    form_data = request.get_form_data()

    file = form_data.get("file")
    if not file:
        return response_formatter.error('No file provided', 400)

    upload_file = upload_file_to_disk(file)
    file_body = create_files_body(form_data, upload_file, organization_user)
    files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

    try:
        create_file = files_repo.transact("POST", data=file_body)
        if create_file:
            return response_formatter.success(create_file, 'File created successfully.', 200)
        else:
            return response_formatter.error('File creation failed.', 400)

    except Exception as e:
        return response_formatter.error(str(e), 500)
