import asyncio
import logging
import json

from typing import Dict, Any, List, Union, Literal
from datetime import datetime
from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol

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
        raise NotImplementedError


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
        """Process a request and return an event"""
        events = self.request_to_events(request)
        responses = []
        for event in events:
            responses.extend(self.process_event(event))
        return responses

    def request_to_events(
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
        """Convert a request to an event"""
        return [request]

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
        """Process an event and return one or more responses"""
        return [event]

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
        return self.process_request(request)


class Server:
    host: str = "localhost"
    port: int = 8765

    async def handle_connection(self, websocket):
        async for raw_request in websocket:
            LOGGER.debug(f"{websocket.remote_address}: {raw_request}")
            decoded_request = json.loads(raw_request)
            decoded_request["sender"] = websocket
            await self.handle_request(decoded_request)

        self.connections.remove(websocket)
        LOGGER.debug(f"{websocket.remote_address} disconnected")
        await websocket.close()

    async def handle_request(
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
        """Handle a request and if needed send a response"""
        raise NotImplementedError

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
    ):
        receiver: WebSocketServerProtocol = response.get("receiver")
        if receiver is None:
            LOGGER.debug(f"No receiver for response: {response}")
        else:
            response = {**response, "receiver": None}
            await receiver.send(json.dumps(response))

    async def _run(self):
        async with serve(self.handle_connection, self.host, self.port):
            await asyncio.Future()

    def start(self) -> None:
        asyncio.run(self._run())


class SubjectServer(Server):
    def __init__(self, subscribers: List[Subscriber]) -> None:
        self.subscribers = subscribers
        super().__init__()

    async def handle_request(
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
        """Handle a request and return responses"""
        responses = []
        for subscriber in self.subscribers:
            response = subscriber.update(request)
            responses.extend(response)
        return responses


if __name__ == "__main__":
    game_server = GameServer()
    server = SubjectServer([game_server])
    server.start()
