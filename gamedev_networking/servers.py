import asyncio
import logging
import json

from typing import Dict, Any, List, Union, Literal
from datetime import datetime
from websockets.server import serve

logging.basicConfig(format=f"[{datetime.now()}] " + "%(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")


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


class GameServer(Subscriber):
    def process_request(
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
        """Process a request and return an event"""
        event = self.request_to_event(request)
        return self.process_event(event)

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
        if method in ["echo", "init"]:
            return {
                "method": method,
                "body": request.get("body"),
                "sender": request.get("target"),
                "target": request.get("sender"),
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
        if method in ["echo", "init"]:
            return {
                "method": method,
                "body": event.get("body"),
                "sender": event.get("target"),
                "target": event.get("sender"),
            }

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
        return self.process_request(request)


class Server:
    host: str = "localhost"
    port: int = 8765

    async def handle_connection(self, websocket):
        raw_request = await websocket.recv()
        LOGGER.debug(f"{websocket.remote_address}: {raw_request}")
        decoded_request = json.loads(raw_request)
        self.on_connection(decoded_request)

        async for raw_request in websocket:
            LOGGER.debug(f"{websocket.remote_address}: {raw_request}")
            decoded_request = json.loads(raw_request)
            responses = self.handle_request(decoded_request)
            for response in responses:
                await self.send_response(response, websocket)

    def on_connection(
        self,
        decoded_request: Dict[
            Union[
                Literal["method"], Literal["body"], Literal["sender"], Literal["target"]
            ],
            Any,
        ],
    ) -> None:
        assert decoded_request["method"] == "init"

    def handle_request(
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
        """Handle a request and return responses"""
        return request

    async def send_response(
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
        websocket,
    ):
        await websocket.send(json.dumps(response))

    async def _run(self):
        async with serve(self.handle_connection, self.host, self.port):
            await asyncio.Future()

    def start(self) -> None:
        asyncio.run(self._run())


class SubjectServer(Server):
    def __init__(self, subscribers: List[Subscriber]) -> None:
        self.subscribers = subscribers
        super().__init__()

    def handle_request(
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
        """Handle a request and return responses"""
        responses = []
        for subscriber in self.subscribers:
            response = subscriber.update(request)
            responses.append(response)
        return responses


if __name__ == "__main__":
    game_server = GameServer()
    server = SubjectServer([game_server])
    server.start()
