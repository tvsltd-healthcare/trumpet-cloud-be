from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

def execute(request: IRequest):
    """
    Approves a user's status and sends a verification email.

    This function handles an incoming request to approve a user's status
    by updating their record in the database. After a successful update,
    it sends an email notification to the user. The request must contain
    a valid JSON body with the user's ID.

    Args:
        request (IRequest): The incoming HTTP request object which must
            include a JSON body with a `user_id` key.

    Returns:
        dict: A formatted response containing the result of the operation.
            - Returns 400 if the request body is missing or malformed.
            - Returns 400 if the user is not found.
            - Returns 201 if the user is successfully updated and email is sent.
            - Returns 500 in case of any internal errors during processing.
    """
    body = request.get_json()

    user_id = body.get('user_id')
    status = body.get('status')
    if not user_id or not status:
        return ResponseFormatter().error("Request isn't valid", 400)

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Users")

    try:
        user = user_repo.get({'id': user_id}, False)
        if not user:
            return ResponseFormatter().success({}, 'User not found', 400)

        user_status_update = user_repo.transact(
            "PATCH",
            data={'status': status},
            query={'id': user.get('id')}
        )

        email_service = EmailServiceManager.get()
        email_body = f"Hello, your token is"

        status = user_status_update.get('status', '').strip().lower()
        print('status', status)


        if status == 'approved':
            print('=================>>>>', 'Approved')
            email_service.send_email(user.get('email'), email_body, type='approved_registration')
        elif status == 'disapproved':
            print('=================>>>>', 'DisApproved')
            email_service.send_email(user.get('email'), email_body, type='disapproved_registration')
        else:
            return

        return ResponseFormatter().success({}, 'User status updated successfully.', 201)
    except Exception as e:
        print(e)
        return ResponseFormatter().error(str(e), 500)