import json
from typing import List, Dict, Any, Union, Literal

from gamedev_networking.clients import GameClient, Client


class TicTacToeGameClient(GameClient):
    def update_ui(
        self,
        response: Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ],
    ) -> List[
        Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ]
    ]:
        output_events = []
        events = self.response_to_events(response)
        for event in events:  # TODO: handle multiple events
            method = event.get("method")
            if method is None:
                raise ValueError("Response does not contain a method")
            if method == "set_username":
                if event.get("body").get("status") == "success":
                    self.username = event.get("body").get("username")
                    print(f"Username set to {self.username}")
                    return []
                if event.get("body").get("status") == "error":
                    print(event.get("body").get("message"))
                    return []
                print("Unknown status")
                return []
            if method == "lobby":
                print(event.get("body"))
                return []

            print(event)
            output_event = input(">> ")
            if output_event:
                output_event = json.loads(output_event)
                output_events.append(output_event)
        return output_events

    def response_to_events(
        self,
        response: Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ],
    ) -> List[
        Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ]
    ]:
        return super().response_to_events(response)


class TicTacToeClient(Client): ...


if __name__ == "__main__":
    game_client = TicTacToeGameClient()
    client = TicTacToeClient(game_client)
    initial_request = {
        "method": "auth",
        "body": {"username": "test", "password": "test"},
        "sender": None,  # to be defined after server receives the request
        "target": "127.0.0.1",
    }
    initial_request_1 = {
        "method": "set_username",
        "body": {"username": "ili"},
        "sender": None,  # to be defined after server receives the request
        "target": "127.0.0.1",
    }
    initial_request_2 = {
        "method": "lobby",
        "body": {},
        "sender": None,  # to be defined after server receives the request
        "target": "127.0.0.1",
    }
    client.add_request(initial_request_1)
    client.add_request(initial_request_2)
    client.start()
