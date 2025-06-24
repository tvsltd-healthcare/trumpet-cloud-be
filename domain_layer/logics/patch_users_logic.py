import time
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.response_formatter_interface import IResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.websocket_pool_manager import WebsocketPoolManager


APPROVED_STATUS = "approved"

@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    response_formatter: IResponseFormatter = ResponseFormatter()

    id_dict = request.get_path_params()
    user = repo.get(id_dict)
    
    if not user:
        return response_formatter.error("User not found.", 404)
    
    user_status = user['status']

    updated_user = repo.patch(entity, id_dict)
    updated_user_status = updated_user['status']

    if updated_user_status == APPROVED_STATUS and updated_user_status != user_status:
        _notify_user_chanel(user['id'])

    return response_formatter.success( updated_user, 'Entity updated successfully', 200 )


def _notify_user_chanel(user_id):
    websocket_pool = WebsocketPoolManager.get()

    websocket_pool.broadcast_json(f'users/{user_id}', {
        'type': 'user_approved',
        'created_at': time.time() * 1000,
    })
