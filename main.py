# main.py
import asyncio
from app_layer_entrypoint import launch_app_layer

if __name__ == "__main__":
    asyncio.run(launch_app_layer())