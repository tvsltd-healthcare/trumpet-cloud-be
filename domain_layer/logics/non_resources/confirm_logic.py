
import os
import anyio

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
import jwt 
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def validate_jwt_token(token, secret_key):
    try:
        # Verify and decode the token
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        print("Token is valid. Payload:", decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired")
        return None
    except jwt.InvalidSignatureError:
        print("Error: Invalid signature (wrong secret key or tampered token)")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Error: Invalid token - {str(e)}")
        return None
    
def execute(request):
    # todo: need to fix this implementation
    # todo: the request implementation should come from wrap-restify
    body = anyio.from_thread.run(request.json)
    decode_token = validate_jwt_token(body.get("token"), JWT_SECRET)
    email = decode_token["email"]
    
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    user = user_repo_invoker.get({ "email": email }, False)
    if not user:
        auth_getter_adapter = AuthManager.get()
        token = auth_getter_adapter.generate_token({"email": email})
        return {
            "message": "User token verify successfully.",
            "data": token,
            "status_code": 200,
        }
    else:
        return {
            "message": "User already exits",
            "status_code": 403,
        }


