from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.parse_token import token_parser
from domain_layer.websocket_pool_manager import WebsocketPoolManager

def execute(websocket):
    websocket.send("👋 Processing Websocket Connection!")

    auth_header = websocket.get_headers().get("authorization")
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get("user_id")
    
    if current_user_id:
        websocket_pool = WebsocketPoolManager.get()
        websocket_pool.register(f'users/{current_user_id}', websocket)
    else:
        print('Websocket cannot be registered!')
        websocket.close()

    return
