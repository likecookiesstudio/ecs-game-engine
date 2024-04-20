from typing import Dict, Union, Literal, Any

from gamedev_networking.clients import GameClient, Client


class TicTacToeGameClient(GameClient):
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
        method = response.get("method")
        if method is None:
            raise ValueError("Response does not contain a method")
        if method == "echo":
            return []
        if method == "init":
            return []
        if method == "auth":
            return []
        if method == "join_lobby":
            return []
        if method == "start_game":
            return []

        event = response
        return [event]


if __name__ == "__main__":
    # import threading

    # def input_loop():
    #     while True:
    #         raw_request = input(">> ")
    #         request = json.loads(raw_request)
    #         client.add_request(request)

    game_client = GameClient()
    client = Client(game_client)
    # input_thread = threading.Thread(target=input_loop, args=(client,))
    initial_request = {
        "method": "auth",
        "body": {"username": "test", "password": "test"},
        "sender": "127.0.0.1",
        "target": "127.0.0.1",
    }
    initial_request = {
        "method": "init",
        "body": {"message": "test"},
        "sender": "127.0.0.1",
        "target": "127.0.0.1",
    }
    client.add_request(initial_request)
    client.add_request(initial_request)
    # input_thread.start()
    client.start()
