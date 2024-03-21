import asyncio
from websockets.sync.client import connect

from utils.networking import Request, Response


def hello():
    with connect("ws://localhost:8765") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")


hello()


class Client:
    def __init__(self) -> None:
        pass

    def send_request(self, request: Request) -> None:
        """send a request to the server"""

    def receive_response(self, response: Response) -> None:
        """receive a response from the server"""
