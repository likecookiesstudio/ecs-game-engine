import logging
from typing import List, Dict, Any


class TicTacToeGameClient(GameClient): ...


class TicTacToeClient(Client): ...


class TicTacToeServer(SubjectServer): ...


class TicTacToeGameServer(GameServer):
    players: Dict[str, Dict[str, Any]] = {
        "X": {"websocket": None, "username": None},
        "O": {"websocket": None, "username": None},
    }
    player_markers: tuple[str, str] = ("X", "O")
    current_player: str = "X"

    def __init__(self, event_handlers: List[EventHandler]) -> None:
        self.event_handlers = event_handlers
        super().__init__(event_handlers)

    def authenticate(self, username: str) -> List[Event]:
        if username in self.players:
            # raise ValueError(f"User {username} is already authenticated")
            logging.warning(f"User {username} is already authenticated")
            return
        player_marker = (
            "X"
            if self.players["X"]["username"] is None
            else ("O" if self.players["O"]["username"] is None else None)
        )
        if player_marker is None:
            raise ValueError("No available player marker")
        self.players[player_marker]["username"] = username
        logging.info(f"User {username} will be playing as {player_marker}")
        return [
            # TODO: return a response to confirm the authentication
            Authentication(username, player_marker)
        ]


class Auth(Event):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__()

    def occur(self, game_server: TicTacToeGameServer) -> None:
        game_server.authenticate(self.username)
        print(f"User {self.username} is authenticated")


class AuthSuccess(Event):
    def __init__(self, username: str, player_marker: str) -> None:
        self.username = username
        self.player_marker = player_marker
        super().__init__()

    def occur(self, game_server: TicTacToeGameServer) -> None:
        game_server.authenticate(self.username)
        print(f"User {self.username} is authenticated")


class Move(Event):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__()

    def occur(self, game_server: TicTacToeGameServer) -> None:
        game_server.move(self.x, self.y)
        print(f"User {game_server.current_player} moved to {self.x}, {self.y}")


class Update(Event):
    def __init__(self, board: List[List[str]]) -> None:
        self.board = board
        super().__init__()

    def occur(self, game_server: TicTacToeGameServer) -> None:
        game_server.apply_event(
            [self]
        )  # TODO: remove apply_event and use queue_next_request or something else
        print(f"Board: {self.board}")


requests = [{"method": "auth", "event": Auth}, {"method": "move", "event": Move}]
responses = [
    {"method": "update", "event": Update},  # update the board
    {"method": "illegal_move", "event": Move},  # illegal move
    {"method": "game_over", "event": Update},  # game over
]


class TicTacToeEventHandler(EventHandler):
    def _request_to_event(self, json_request: Dict[str, Any]) -> List[Event]:
        method = json_request["method"]
        if method == "auth":
            return [Auth(json_request["username"])]
        elif method == "move":
            return [Move(json_request["x"], json_request["y"])]
        else:
            logging.warning(f"Unknown method: {method}")
            return []

    def _event_to_response(self, event: List[Event]) -> List[Dict[str, Any]]:
        responses = []
        for event in event:
            if isinstance(event, Auth):
                responses.append({"method": "auth", "event": event})
            elif isinstance(event, Move):
                responses.append({"method": "move", "event": event})
            elif isinstance(event, Update):
                responses.append({"method": "update", "event": event})
            else:
                logging.warning(f"Unknown event: {event}")
        return responses
