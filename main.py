class Client:
    def __init__(self) -> None:
        pass

    def send_request(self, request) -> None:
        """send a request to the server"""

    def receive_response(self, response) -> None:
        """receive a response from the server"""


class Server:
    def __init__(self) -> None:
        pass

    def receive_request(self, request) -> None:
        """receive client's request"""

    def send_response(self, response) -> None:
        """send a response to client's request"""


class Game:

    def __init__(self) -> None:
        pass

    def update(self) -> None:
        pass


class Event: ...


class EventHandler: ...
