from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class TicTacToeGame:
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

    def make_move(self, event):
        if self.game_over:
            return
        self.board[i][j] = player
        self.ui.current_player = player
        if self.check_win(player):
            event = {"method": "winner", "player": player}
            self.ui.handle_event(event)
            print("Player {} wins!".format(player))
            self.game_over = True
            return
        if self.check_tie():
            event = {"method": "tie"}
            self.ui.handle_event(event)
            print("Tie!")
            self.game_over = True
            return
        event = {"method": "make_move", "i": i, "j": j, "player": player}
        self.ui.handle_event(event)
        self.current_player = "X" if self.current_player == "O" else "O"


class TicTacToeUI(GridLayout):
    def __init__(self, **kwargs):
        self.game: TicTacToeGame = None
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
            button.text = self.current_player
            button_list = [row for row in self.board if button in row][0]
            i = self.board.index(button_list)
            j = button_list.index(button)
            self.game.make_move(i, j, self.current_player)

    def handle_event(self, event):
        if event["method"] == "winner":  # {"method": "winner", "player": "X"}
            self.game_over = True
            return
        if event["method"] == "tie":  # {"method": "tie"}
            self.game_over = True
            return
        if (
            event["method"] == "make_move"
        ):  # {"method": "make_move", "i": 0, "j": 0, "player": "X"}
            i, j, player = event["i"], event["j"], event["player"]
            self.board[i][j].text = player
            self.current_player = "X" if self.current_player == "O" else "O"
            return


class TicTacToeApp(App):
    def build(self):
        ui = TicTacToeUI()
        game = TicTacToeGame(ui)
        return ui


if __name__ == "__main__":
    TicTacToeApp().run()
