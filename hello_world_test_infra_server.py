import asyncio
import logging
import json

from pydantic import BaseModel
from typing import Dict, Any, List, Union, Literal
from datetime import datetime
from websockets.server import serve

logging.basicConfig(format=f"[{datetime.now()}] " + "%(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")


class Event(BaseModel):
    pass


class EchoEvent(Event):
    message: str
    meta: Dict[str, Any] = {}


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
    def process_reqeust(self, request: Dict[str, Any]) -> Event:
        """Process a request and return an event"""
        event = self.request_to_event(request)
        return self.process_event(event)

    def request_to_event(self, request: Dict[str, Any]) -> Event:
        """Convert a request to an event"""
        method = request.get("method")
        if method is None:
            raise ValueError("Method not found")
        if method == "echo":
            return EchoEvent(message=request["message"])
        else:
            raise ValueError(f"Method not found: {method}")

    def process_event(self, event: Event) -> Dict[str, Any]:
        """Process an event and return a response"""
        if isinstance(event, EchoEvent):
            return {"method": "echo", "message": event.message}
        else:
            raise ValueError(f"Event not found: {event}")

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
        return self.process_reqeust(request)


class Server:
    host: str = "localhost"
    port: int = 8765

    async def receive_request(self, websocket):
        decoded_requests = []
        async for raw_request in websocket:
            LOGGER.debug(f"{websocket.remote_address}: {raw_request}")
            decoded_request = json.loads(raw_request)
            decoded_requests.append(decoded_request)
        return decoded_requests

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

    async def main(self, websocket):
        requests = await self.receive_request(websocket)
        responses = await asyncio.gather(
            *[self.handle_request(request) async for request in requests]
        )
        async for response in responses:
            target = response.pop("target", None)
            if target is None:
                continue
            await self.send_response(response, target)

    async def _run(self):
        async with serve(self.main, self.host, self.port):
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
