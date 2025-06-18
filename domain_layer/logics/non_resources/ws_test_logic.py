from domain_layer.abstractions.request_interface import IRequest


# from fastapi import WebSocket


def execute(request: IRequest):
    print("okkkk")
    return
    # print("kkkk")
    # # Accept connection
    # accept_func = websocket.accept()
    # accept_func()
    #
    # try:
    #     print('okkkk')
    #     while True:
    #         # Receive message
    #         receive_func = websocket.receive_text()
    #         message = receive_func()
    #
    #         # Process message (echo back with prefix)
    #         response = f"Echo: {message}"
    #
    #         # Send response
    #         send_func = websocket.send_text(response)
    #         send_func()
    #
    # except Exception as e:
    #     print(f"WebSocket error: {e}")
    # finally:
    #     close_func = websocket.close()
    #     close_func()
