from domain_layer.abstractions.request_interface import IRequest


# from fastapi import WebSocket


async def my_websocket_handler(websocket):
    await websocket.accept()
    message = await websocket.receive_text()
    await websocket.send_text(f"Echo: {message}")
    await websocket.close()
