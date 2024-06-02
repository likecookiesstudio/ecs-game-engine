import asyncio
import logging
import json

from typing import Dict, Any, Union, Literal
from datetime import datetime
from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol

logging.basicConfig(format=f"[{datetime.now()}] " + "%(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")


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
