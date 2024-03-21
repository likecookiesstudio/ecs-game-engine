import asyncio
import logging
from datetime import datetime
from websockets.server import serve

from utils.networking import Request, Response

logging.basicConfig(format=f"[{datetime.now()}] " + "%(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")


class Server:
    host: str = "localhost"
    port: int = 8765

    def __init__(self) -> None:
        asyncio.run(self._run())

    def receive_request(self, request: Request) -> None:
        """receive client's request"""

    def send_response(self, response: Response) -> None:
        """send a response to client's request"""

    def process_message(self, raw_message):
        return raw_message

    async def main(self, websocket):
        async for message in websocket:
            LOGGER.debug(message)
            processed_message = self.process_message(message)
            LOGGER.debug(processed_message)
            await websocket.send(processed_message)

    async def _run(self):
        async with serve(self.main, self.host, self.port):
            await asyncio.Future()


if __name__ == "__main__":
    s = Server()
