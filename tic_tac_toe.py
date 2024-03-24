from base.game_clients import GameClient
from base.clients import Client
from base.servers import SubjectServer
from base.event_handlers import EventHandler
from base.game_servers import GameServer


class TicTacToeGameClient(GameClient): ...


class TicTacToeClient(Client): ...


class TicTacToeServer(SubjectServer): ...


class TicTacToeEventHandler(EventHandler): ...


class TicTacToeGameServer(GameServer): ...
