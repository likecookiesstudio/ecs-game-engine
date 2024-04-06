import asyncio
import logging
import json

from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from websockets.server import serve

logging.basicConfig(format=f"[{datetime.now()}] " + "%(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")


class Event(BaseModel):
    pass


class EchoEvent(Event):
    message: str
    meta: Dict[str, Any] = {}


class GameServer:
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



class Server:
    host: str = "localhost"
    port: int = 8765

    async def main(self, websocket):
        async for raw_request in websocket:
            LOGGER.debug(f"{websocket.remote_address}: {raw_request}")
            decoded_request = json.loads(raw_request)
            request = {**decoded_request, "websocket": websocket.remote_address}
            response
            await websocket.send(response)

    async def _run(self):
        async with serve(self.main, self.host, self.port):
            await asyncio.Future()

    def start(self) -> None:
        asyncio.run(self._run())
    
    def _handle_requests(self, ):


if __name__ == "__main__":
    server = Server()
    server.start()
