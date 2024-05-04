from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class TicTacToeGame(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 3
        self.cols = 3
        self.board = [[None for _ in range(3)] for _ in range(3)]
        super(TicTacToeGame, self).__init__(**kwargs)
        self.current_player = "X"
        self.game_over = False

        for i in range(3):
            for j in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.on_button_press)
                self.board[i][j] = button
                self.add_widget(button)

    def on_button_press(self, button):
        if button.text == "":
            button.text = self.current_player
            if self.check_win(button.text):
                print("Player {} wins!".format(button.text))
                self.game_over = True
            elif self.check_draw():
                print("Draw!")
                self.game_over = True
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def check_win(self, player):
        for i in range(3):  # row
            if all(self.board[i][j].text == player for j in range(3)):
                return True
        for j in range(3):  # column
            if all(self.board[i][j].text == player for i in range(3)):
                return True
        if all(self.board[i][i].text == player for i in range(3)) or all(
            self.board[i][2 - i].text == player for i in range(3)
        ):  # diagonals
            return True
        return False

    def check_draw(self):
        return (
            all([self.board[i][j].text != "" for i in range(3) for j in range(3)])
            and not self.check_win("X")
            and not self.check_win("O")
        )


class TicTacToeApp(App):
    def build(self):
        game = TicTacToeGame()
        return game


if __name__ == "__main__":
    TicTacToeApp().run()
