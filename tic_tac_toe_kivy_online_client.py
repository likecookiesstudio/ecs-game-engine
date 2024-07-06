from typing import Any, Dict, Literal
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from gamedev_networking.clients import Client


class TicTacToeGameLogicProxy(Client):
    def __init__(self, ui):
        self.ui: TicTacToeUI = ui
        super(TicTacToeGameLogicProxy, self).__init__()

    def process_response(
        self, response: Dict[Literal["method", "body", "sender", "target"], Any]
    ) -> None:
        self.ui.handle_event(response)

    def handle_event(
        self, event: Dict[Literal["method", "body", "sender", "target"], Any]
    ):
        self.send_request(event)


class TicTacToeUI(GridLayout):
    def __init__(self, **kwargs):
        self.game: TicTacToeGameLogicProxy = None
        self.rows = 3
        self.cols = 3
        self.board = [[None for _ in range(3)] for _ in range(3)]
        super(TicTacToeUI, self).__init__(**kwargs)
        self.current_player = None
        self.player_tag = None  # to be assigned in the game logic. Either "X" or "O"
        self.game_over = False

        for i in range(3):
            for j in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.on_button_press)
                self.board[i][j] = button
                self.add_widget(button)

    def on_button_press(self, button):
        if self.game_over:
            return

        if (self.player_tag is not None) and self.player_tag != self.current_player:
            print(f"Player {self.player_tag} is not the current player.")
            return

        if button.text == "":
            button_list = [row for row in self.board if button in row][0]
            event = {
                "method": "make_move",
                "body": {
                    "i": self.board.index(button_list),
                    "j": button_list.index(button),
                    "player": self.current_player,
                },
            }
            self.game.handle_event(event)

    def handle_event(self, event):
        print(event)
        body = event["body"]
        if event["method"] == "join":
            if self.player_tag is not None:
                print(f"Player {self.player_tag} is already assigned.")
                return
            self.player_tag = body["tag"]
            self.current_player = body["current_player"]
            return

        i, j, player = (
            body.get("i"),
            body.get("j"),
            body.get("player"),
        )
        if (
            event["method"] == "winner"
        ):  # {'method': 'winner', 'i': 1, 'j': 0, 'player': 'X', 'sender': None, 'receiver': None}
            self.game_over = True
            self.board[i][j].text = player
            return

        if (
            event["method"] == "tie"
        ):  # {'method': 'tie', 'i': 2, 'j': 2, 'player': 'X', 'sender': None, 'receiver': None}
            self.game_over = True
            self.board[i][j].text = player
            return

        if (
            event["method"] == "make_move"
        ):  # {"method": "make_move", "i": 0, "j": 0, "player": "X"}
            self.current_player = "X" if self.current_player == "O" else "O"
            self.board[i][j].text = player
            return

    def set_game(self, game: TicTacToeGameLogicProxy):
        self.game = game

    def start(self):
        # setup
        self.game.send_request({"method": "join", "body": {}})


class TicTacToeApp(App):
    def build(self):
        ui = TicTacToeUI()
        game = TicTacToeGameLogicProxy(ui)
        ui.set_game(game)
        ui.start()
        return ui


if __name__ == "__main__":
    TicTacToeApp().run()
