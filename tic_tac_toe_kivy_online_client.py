from typing import Any, Dict, Literal
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


from gamedev_networking.clients import Client


class TicTacToeClient(Client):
    def __init__(self, ui):
        self.ui: TicTacToeUI = ui
        self.ui.game = self
        super(TicTacToeClient, self).__init__()

    def process_response(
        self, response: Dict[Literal["method", "body", "sender", "target"], Any]
    ) -> None:
        self.ui.handle_event(response)

    def make_move(self, i, j, player):
        self.send_request(
            {
                "method": "make_move",
                "i": i,
                "j": j,
                "player": player,
            }
        )


class TicTacToeUI(GridLayout):
    def __init__(self, **kwargs):
        self.game: TicTacToeClient = None
        self.rows = 3
        self.cols = 3
        self.board = [[None for _ in range(3)] for _ in range(3)]
        super(TicTacToeUI, self).__init__(**kwargs)
        self.current_player = "X"
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
        if button.text == "":
            button_list = [row for row in self.board if button in row][0]
            i = self.board.index(button_list)
            j = button_list.index(button)
            self.game.make_move(i, j, self.current_player)

    def handle_event(self, event):
        print(event)
        i, j, player = event.get("i"), event.get("j"), event.get("player")
        if (
            event["method"] == "winner"
        ):  # {'method': 'winner', 'i': 1, 'j': 0, 'player': 'X', 'sender': None, 'receiver': None}
            self.game_over = True

        elif (
            event["method"] == "tie"
        ):  # {'method': 'tie', 'i': 2, 'j': 2, 'player': 'X', 'sender': None, 'receiver': None}
            self.game_over = True

        elif (
            event["method"] == "make_move"
        ):  # {"method": "make_move", "i": 0, "j": 0, "player": "X"}
            self.current_player = "X" if self.current_player == "O" else "O"
        self.board[i][j].text = player


class TicTacToeApp(App):
    def build(self):
        ui = TicTacToeUI()
        game = TicTacToeClient(ui)
        return ui


if __name__ == "__main__":
    TicTacToeApp().run()
