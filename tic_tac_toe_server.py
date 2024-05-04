from typing import List, Dict, Any, Union, Literal
from websockets.legacy.server import WebSocketServerProtocol


from gamedev_networking.servers import GameServer, SubjectServer


# class TicTacToeGameServer(GameServer):
#     def request_to_events(
#         self,
#         request: Dict[
#             Union[
#                 Literal["method"],
#                 Literal["body"],
#                 Literal["sender"],
#                 Literal["target"],
#             ],
#             Any,
#         ],
#     ) -> Dict[
#         Union[
#             Literal["method"],
#             Literal["body"],
#             Literal["sender"],
#             Literal["target"],
#         ],
#         Any,
#     ]:
#         """Convert a request to an event"""
#         method = request.get("method")
#         if method is None:
#             raise ValueError("Method not found")
#         if method == "echo":
#             return {
#                 "method": method,
#                 "body": request.get("body"),
#                 "sender": request.get("target"),
#                 "target": request.get("sender"),
#             }

#     def process_event(
#         self,
#         event: Dict[
#             Union[
#                 Literal["method"],
#                 Literal["body"],
#                 Literal["sender"],
#                 Literal["target"],
#             ],
#             Any,
#         ],
#     ) -> Dict[
#         Union[
#             Literal["method"],
#             Literal["body"],
#             Literal["sender"],
#             Literal["target"],
#         ],
#         Any,
#     ]:
#         """Process an event and return a response"""
#         method = event.get("method")
#         if method is None:
#             raise ValueError("Method not found")
#         if method == "echo":
#             return {
#                 "method": method,
#                 "body": event.get("body"),
#                 "sender": event.get("target"),
#                 "target": event.get("sender"),
#             }


class TicTacToeGameServer(GameServer):
    lobby: Dict[Union[Literal["players"], Literal["rooms"]], List[Dict[str, Any]]] = {
        "players": [],
        "rooms": [],
    }
    players: Dict[Union[Literal["X"], Literal["O"]], Dict[str, Any]] = {
        "X": {"websocket": None, "username": None},
        "O": {"websocket": None, "username": None},
    }
    player_markers: tuple[Literal["X"], Literal["O"]] = ("X", "O")
    current_player: Union[Literal["X"], Literal["O"]] = "X"
    board: List[List[Union[Literal["X"], Literal["O"], None]]] = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    def request_to_events(
        self,
        request: Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ],
    ) -> List[
        Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ]
    ]:
        """Convert a request to an event"""
        method = request.get("method")
        if method is None:
            raise ValueError("Method not found")

        if method == "set_username":
            return [
                {
                    "method": method,
                    "body": request.get("body"),  # {"username": "me"}
                    "sender": request.get("target"),
                    "target": request.get("sender"),
                }
            ]
        if method == "lobby":
            return [
                {
                    "method": method,
                    "body": request.get("body"),  # {}
                    "sender": request.get("target"),
                    "target": request.get("sender"),
                }
            ]

        return [
            {
                "method": "invalid_method",
                "body": {"status": "error", "message": "Invalid method"},
                "sender": request.get("target"),
                "target": request.get("sender"),
            }
        ]

    def process_event(
        self,
        event: Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ],
    ) -> List[
        Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ]
    ]:
        method = event.get("method")
        if method is None:
            raise ValueError("Method not found")

        player = [
            player
            for player in self.lobby["players"]
            if player["websocket"] == event.get("target")
        ]
        player = player[0] if player else dict()

        if method == "set_username":
            # username already set
            if not (player.get("username") is None):
                return {
                    "method": method,
                    "body": {"status": "error", "message": "Username already set"},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            username = event.get("body").get("username")
            # invalid username
            if (not isinstance(username, str)) or username == "":
                return {
                    "method": method,
                    "body": {"status": "error", "message": "Invalid username"},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            # username too long
            if len(username) > 16:
                return {
                    "method": method,
                    "body": {"status": "error", "message": "Username too long"},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            # username too short
            if len(username) < 3:
                return {
                    "method": method,
                    "body": {"status": "error", "message": "Username too short"},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            # username already taken
            if username in [player["username"] for player in self.lobby["players"]]:
                return {
                    "method": method,
                    "body": {"status": "error", "message": "Username already taken"},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }

            self.lobby["players"].append(
                {
                    "username": username,
                    "websocket": event.get("sender"),
                }
            )
            return [
                {
                    "method": method,
                    "body": {"status": "success", "username": username},
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            ]

        if method == "lobby":
            secret_player_attributes = {"websocket"}
            players = []
            for player in self.lobby["players"]:
                for key, value in player.items():
                    if key not in secret_player_attributes:
                        players.append({key: value})

            secret_room_attributes = {"password"}
            rooms = []
            for room in self.lobby["rooms"]:
                for key, value in room.items():
                    if key not in secret_room_attributes:
                        rooms.append({key: value})
            return [
                {
                    "method": method,
                    "body": {
                        "players": players,
                        "rooms": rooms,
                    },
                    "sender": event.get("target"),
                    "target": event.get("sender"),
                }
            ]


class TicTacToeServer(SubjectServer):
    async def on_connection(
        self,
        decoded_request: Dict[
            Literal["method"] | Literal["body"] | Literal["sender"] | Literal["target"],
            Any,
        ],
        websocket: WebSocketServerProtocol,
    ) -> None:
        responses = self.handle_request(decoded_request)
        for response in responses:
            await self.send_response(response, websocket)


if __name__ == "__main__":
    game_server = TicTacToeGameServer()
    subject_server = TicTacToeServer([game_server])
    subject_server.start()
