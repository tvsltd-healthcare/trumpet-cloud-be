
import anyio

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Mailtrap configuration
MAILTRAP_HOST = os.getenv("MAILTRAP_HOST")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT"))
MAILTRAP_USERNAME = os.getenv("MAILTRAP_USERNAME")
MAILTRAP_PASSWORD = os.getenv("MAILTRAP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

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
        token = auth_getter_adapter.generate_token({"user_id": email})
        token_value = token["token"] if isinstance(token, dict) else token
        
        # Create email message
        # custom template
        msg = MIMEText(token_value, "html")
        msg["Subject"] = "Test email"
        msg["From"] = SENDER_EMAIL
        msg["To"] = email

    else:
        return {
            "message": "User already exits",
            "status_code": 403,
        }

    try:
        # Connect to Mailtrap SMTP server
        with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
            server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
            server.send_message(msg)
        return {"message": "Email sent successfully to Mailtrap"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


