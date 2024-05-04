from gamedev_networking.servers import Server


class TicTacToeGame:
    connections = {}

    def __init__(self, ui):
        self.ui = ui
        self.ui.game = self
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False

    def check_win(self, player):
        for i in range(3):  # row
            if all(self.board[i][j] == player for j in range(3)):
                return True
        for j in range(3):  # column
            if all(self.board[i][j] == player for i in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(
            self.board[i][2 - i] == player for i in range(3)
        ):  # diagonals
            return True
        return False

    def check_tie(self):
        return (
            all([self.board[i][j] != "" for i in range(3) for j in range(3)])
            and not self.check_win("X")
            and not self.check_win("O")
        )

    async def handle_event(self, event) -> None:
        if self.game_over:
            return
        sender = event.get("sender")
        if sender is None:
            print(f"No sender for event: {event}")
            return
        
        if not (sender in TicTacToeGame.connections):
            if len(TicTacToeGame.connections) == 0:
                name = "X"
            elif len(TicTacToeGame.connections) == 1:
                name = "O"
            else:
                print(f"Too many connections: {len(TicTacToeGame.connections)}, event: {event}")
                return
            print(f"Sender {sender} not in connections. Saving as {name}.")
            TicTacToeGame.connections[sender] = {"name": name}

        if len(TicTacToeGame.connections) < 2:
            print(f"Too few connections: {len(TicTacToeGame.connections)}, event: {event}")
            return
        
        if len(TicTacToeGame.connections) > 2:
            print(f"Too many connections: {len(TicTacToeGame.connections)}, event: {event}")
            return
        
        event = {**event, "receiver": sender, "sender": None}
        i, j, player = event["i"], event["j"], event["player"]
        self.board[i][j] = player
        self.ui.current_player = player
        if self.check_win(player):
            print(f"Player {player} wins!")
            response_event = {**event, "method": "winner", "player": player}
            await self.ui.handle_event(response_event)
            print(f"Player {response_event["receiver"]} was updated.")
            receiver = (set(TicTacToeGame.connections.keys()) - {response_event["receiver"]}).pop()
            response_event = {
                **event,
                "method": "winner",
                "player": player,
                "receiver": receiver,
            }
            await self.ui.handle_event(response_event)
            print(f"Player {response_event["receiver"]} was updated.")
            self.game_over = True
            return
        if self.check_tie():
            print("Tie!")
            response_event = {**event, "method": "tie"}
            await self.ui.handle_event(response_event)
            print(f"Player {response_event["receiver"]} was updated.")
            receiver = (set(TicTacToeGame.connections.keys()) - {response_event["receiver"]}).pop()
            response_event = {
                **event,
                "method": "tie",
                "receiver": receiver,
            }
            self.ui.handle_event(response_event)
            print(f"Player {response_event["receiver"]} was updated.")
            self.game_over = True
            return
        response_event = {**event, "method": "make_move", "i": i, "j": j, "player": player}
        await self.ui.handle_event(response_event)
        print(f"Player {response_event["receiver"]} was updated.")

        receiver = (set(TicTacToeGame.connections.keys()) - {response_event["receiver"]}).pop()
        response_event = {**event, "method": "make_move", "i": i, "j": j, "player": player, "receiver": receiver}
        await self.ui.handle_event(response_event)
        print(f"Player {response_event["receiver"]} was updated.")
        
        self.current_player = "X" if self.current_player == "O" else "O"
        # TODO? notify all players which player's turn it is


class TicTacToeServer(Server):
    def __init__(self, **kwargs):
        self.game: TicTacToeGame = None

    async def handle_request(self, request):
        await self.game.handle_event(request)

    async def handle_event(self, event):
        print(event)
        await self.send_response(event)


if __name__ == "__main__":
    ui = TicTacToeServer()
    game = TicTacToeGame(ui)
    ui.start()
