
import os
import anyio
from dotenv import load_dotenv
from fastapi import HTTPException
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")

def execute(request):

    body = anyio.from_thread.run(request.json)
    email = body.get("email")
    query = { "email": email }

    # discovery repo
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    user = user_repo_invoker.get(query, False)

    if not user:
        auth_getter_adapter = AuthManager.get()
        token = auth_getter_adapter.generate_token({"email": email})
        token_value = token["token"] if isinstance(token, dict) else token

        try:
            email_service = EmailServiceManager.get()
            email_service.send_email(email, EMAIL_SUBJECT, token_value, SENDER_EMAIL)
            
            return {
                "message": "Email sent successfully", 
                "status_code": 200
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

    else:
        return {
            "message": "User already exits",
            "status_code": 403,
        }


