from domain_layer.abstractions.websocket_wrapper_interface import IWebSocketWrapper


def execute(websocket: IWebSocketWrapper, msg):
    print("You can receive any websocket incoming message here and work on it")
    print("msg orint from server logi  file:::::", msg)
    websocket.send(msg)
    return
