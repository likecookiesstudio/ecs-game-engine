import json
import threading
from typing import List

from websockets.sync.client import connect

from utils.networking import Request, Response


# def hello():
#     with connect("ws://localhost:8765") as websocket:
#         websocket.send("Hello world!")
#         message = websocket.recv()
#         print(f"Received: {message}")


# hello()


class Client:
    def __init__(self) -> None:
        self.websocket = connect(
            "ws://localhost:8765"
        )  # Remember to .close() in the end

        self.running = True

        self.__requests: List[Request] = []
        self.__responses: List[Response] = []

        self.send_thread = threading.Thread(target=self.__handle_requests)
        self.recv_thread = threading.Thread(target=self.__handle_responses)

        self.send_thread.start()
        self.recv_thread.start()

    def _receive_response(self) -> None:
        """receive a response from the server"""
        return self.websocket.recv()

    def _send_request(self, request: Request) -> None:
        """send a request to the server"""
        return self.websocket.send(request)

    def _decode_response(self, response) -> Response:
        return json.loads(response)

    def _encode_request(self, request: Request):
        return request.json()

    def __handle_requests(self) -> None:
        while self.running:
            while self.__requests:
                request = self._load_next_request()
                encoded_request = self._encode_request(request)
                self._send_request(encoded_request)

    def __handle_responses(self) -> None:
        while self.running:
            response = self._receive_response()
            decoded_response = self._decode_response(response)
            self._queue_response(decoded_response)

    def queue_request(self, request: Request) -> None:
        self.__requests.append(request)

    def _queue_response(self, response: Response) -> None:
        self.__responses.append(response)

    def _load_next_request(self) -> Request:
        return self.__requests.pop(0)

    def start(self, loop_method: callable) -> None:
        loop_method()

    def stop(self) -> None:
        self.running = False
        self.websocket.close()


if __name__ == "__main__":
    from custom_requests import Auth

    class GameMock:
        def __init__(self, client: Client):
            self.client = client

        def loop_method(self):
            auth_req = Auth(username="Denis")
            while True:
                self.client.queue_request(auth_req)
                input("freeze")

    client = Client()
    game = GameMock(client)

    client.start(game.loop_method)
