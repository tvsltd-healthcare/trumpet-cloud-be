from domain_layer.abstractions.websocket_wrapper_interface import IWebSocketWrapper
from domain_layer.utils.parse_token import token_parser
from domain_layer.websocket_pool_manager import WebsocketPoolManager


def execute(websocket: IWebSocketWrapper, msg: str, event: str = 'message_received'):
    # todo: auth: LGTM. VALUR FROM TOKEN
    
    print("You can receive any websocket incoming message here and work on it")
    print("msg orint from server logi  file:::::", msg)
    
    if event == 'message_received':
        websocket.send(msg)
        return
    
    if event == 'socket_closed':
        print('App: Websocket is being cleaned up!')
        user_token = websocket.get_query_params().get("token")
        decoded_token = token_parser(user_token)
        current_user_id = decoded_token.get("user_id")
        
        websocket_pool = WebsocketPoolManager.get()
        websocket_pool.disconnect(f'users/{current_user_id}', websocket)
        print('App: Websocket cleaned up!')
        return
    
    return
