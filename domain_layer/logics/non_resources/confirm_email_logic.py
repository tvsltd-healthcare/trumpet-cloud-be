from fastapi import HTTPException
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter

def execute(request):
    """
    Verifies a user token, checks if the user not exists by email, and generates a new token if not.
    
    Args:
        request: The request object containing a JSON body with a token.
    
    Returns:
        Dict containing message, status_code, and optional data.
    """

    body = request.get_json()
    auth_getter_adapter = AuthManager.get()
    
    try:
        decode_token = auth_getter_adapter.read_data(body.get("token"))
        if not decode_token.get("email"):
            raise ValueError("Email not found in token")
        
        email = decode_token.get("email")
        if not email:
            raise ValueError("Email not found in decoded token")
    
        repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
        user = user_repo_invoker.get({"email": email}, False)
        
        if not user:
            auth_getter_adapter = AuthManager.get()
            # TODO: If not assgin user_id then when we create user then token is not valid in auth middleware
            # Adding user_id = 1 temporary
            token = auth_getter_adapter.generate_token({"email": email, "user_id": 1}) 
            if not token:
                raise RuntimeError("Failed to generate new token")
            
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

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(ve)}")
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(re)}")
    except AttributeError as ae:
        raise HTTPException(status_code=500, detail=f"Invalid attribute access: {str(ae)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
