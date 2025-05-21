from domain_layer.auth_manager import AuthManager
from domain_layer.password_manager import PasswordManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter


def execute(request):

    """
    Handles the password reset functionality for a user based on a valid authentication token.

    This function performs the following steps:
    1. Parses the JSON body from the incoming request.
    2. Authenticates the user by decoding the provided token to extract the user's email.
    3. Fetches the user data from the "Users" repository using the extracted email.
    4. If the user exists, hashes the new password and updates the user record.
    5. Returns appropriate success or error responses.

    Parameters:
        request (flask.Request or similar): The HTTP request object containing a JSON body with:
            - token (str): Authentication token to identify the user.
            - new_password (str): The new password to be set.

    Returns:
        A formatted JSON response with:
            - 200 status code if password reset is successful.
            - 400 status code for missing email or failure in resetting the password.
            - 403 status code if the user does not exist.
            - 500 status code if any unhandled exception occurs.

    Raises:
        This function does not explicitly raise exceptions; all exceptions are caught and returned as error responses.
    """

    body = request.get_json()
    auth_getter_adapter = AuthManager.get()
    response_formatter = ResponseFormatter()

    decode_token = auth_getter_adapter.read_data(body.get("token"))
    email = decode_token.get("email")

    if not email:
        return response_formatter.error('Email missing.',400)

    if decode_token.get('reset_password') is not True:
        return response_formatter.error('You are not eligible to reset password.', 403)

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    try:
        user = user_repo.get({"email": email}, False)
        if user:
            new_password = body.get("new_password")
            password_handler = PasswordManager.get()

            password = password_handler.hash_password(new_password)
            password_reset_body = { "password": password  }

            password_reset = user_repo.transact("PATCH", data=password_reset_body)
            if(password_reset):
                return response_formatter.success( {}, 'Password reset successfully.', 200)
            else:
                return response_formatter.error('Password reset failed', 400)
        else:
            return response_formatter.error('User not exits', 400)
    except Exception as e:
        return response_formatter.error(str(e), 500)
