from typing import Dict, Any, Union, Literal

from gamedev_networking.servers import GameServer, SubjectServer


class TicTacToeGameServer(GameServer):
    def request_to_event(
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
    ) -> Dict[
        Union[
            Literal["method"],
            Literal["body"],
            Literal["sender"],
            Literal["target"],
        ],
        Any,
    ]:
        """Convert a request to an event"""
        method = request.get("method")
        if method is None:
            raise ValueError("Method not found")
        if method == "echo":
            return {
                "method": "echo",
                "body": request.get("body"),
                "sender": request.get("sender"),
                "target": request.get("target"),
            }

    def process_event(
        self,
        event: Dict[
            Union[
                Literal["method"],
                Literal["body"],
                Literal["sender"],
                Literal["target"],
            ],
            Any,
        ],
    ) -> Dict[
        Union[
            Literal["method"],
            Literal["body"],
            Literal["sender"],
            Literal["target"],
        ],
        Any,
    ]:
        """Process an event and return a response"""
        method = event.get("method")
        if method is None:
            raise ValueError("Method not found")
        if method == "echo":
            return {
                "method": "echo",
                "body": event.get("body"),
                "sender": event.get("sender"),
                "target": event.get("target"),
            }


if __name__ == "__main__":
    game_server = GameServer()
    subject_server = SubjectServer([game_server])
    subject_server.start()
