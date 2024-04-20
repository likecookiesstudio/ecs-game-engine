import json
import threading
from typing import List, Any, Dict, Union, Literal

from websockets.sync.client import connect


class Subscriber:
    def update(
        self,
        request: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        pass


class GameClient(Subscriber):
    def update_ui(
        self,
        response: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        output_events = []
        events = self.response_to_events(response)
        for event in events:  # TODO: handle multiple events
            print(event)
            input(">> ")
            output_events.append(event)
        return output_events

    def response_to_events(
        self,
        response: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ):
        event = response
        return [event]


class Client:
    def __init__(self, game_client: GameClient) -> None:
        self.websocket = connect(
            "ws://localhost:8765"
        )  # Remember to .close() in the end

        self.game_client = game_client

        self.running = True

        self.__requests: List[
            Dict[
                Union[
                    Literal["method"],
                    Literal["body"],
                    Literal["sender"],
                    Literal["target"],
                ],
                Any,
            ]
        ] = []
        self.__responses: List[
            Dict[
                Union[
                    Literal["method"],
                    Literal["body"],
                    Literal["sender"],
                    Literal["target"],
                ],
                Any,
            ]
        ] = []

        self.send_thread = threading.Thread(target=self.__handle_requests)
        self.recv_thread = threading.Thread(target=self.__handle_responses)

        self.send_thread.start()
        self.recv_thread.start()

    def __handle_requests(self) -> None:
        while self.running:
            while self.__requests:
                request = self.get_request()
                self.send_request(request)

    def __handle_responses(self) -> None:
        while self.running:
            response = self.receive_response()
            self.add_response(response)

    def receive_response(self) -> Dict[
        Union[
            Literal["method"],
            Literal["body"],
            Literal["sender"],
            Literal["target"],
        ],
        Any,
    ]:
        """receive a response from the server"""
        raw_response = self.websocket.recv()
        return json.loads(raw_response)

    def send_request(
        self,
        request: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        """send a request to the server"""
        encoded_request = json.dumps(request)
        self.websocket.send(encoded_request)

    def add_request(
        self,
        request: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        self.__requests.append(request)

    def add_response(
        self,
        response: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        self.__responses.append(response)

    def get_request(self) -> Dict[
        Union[
            Literal["method"],
            Literal["body"],
            Literal["sender"],
            Literal["target"],
        ],
        Any,
    ]:
        return self.__requests.pop(0)

    def get_response(self) -> Dict[
        Union[
            Literal["method"],
            Literal["body"],
            Literal["sender"],
            Literal["target"],
        ],
        Any,
    ]:
        return self.__responses.pop(0) if self.__responses else None

    def start(self) -> None:
        self.main_client_loop()

    def stop(self) -> None:
        self.running = False
        self.websocket.close()

    def process_response(
        self,
        response: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> None:
        requests = self.game_client.update_ui(response)
        self.__requests.extend(requests)

    def main_client_loop(self) -> None:
        while self.running:
            while self.__responses:
                response = self.get_response()
                self.process_response(response)


if __name__ == "__main__":
    game_client = GameClient()
    client = Client(game_client=game_client)

    initial_request = {
        "method": "start",
        "body": {},
        "sender": "client",
        "target": "server",
    }
    client.add_request(initial_request)

    client.start()
