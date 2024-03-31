import taipy as tp
from itertools import cycle

# Define the Player and Move classes as before

class Player:
    def __init__(self, label, color):
        self.label = label
        self.color = color

class Move:
    def __init__(self, row, col, label=""):
        self.row = row
        self.col = col
        self.label = label

# Assume TicTacToeGame class is defined similarly to before, adapted for Taipy if necessary
# TicTacToeGame logic class adapted for Taipy
class TicTacToeGame:
    def __init__(self, players, board_size=3):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = [[Move(row, col) for col in range(board_size)] for row in range(board_size)]
        self._has_winner = False
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        # Logic to generate winning combinations remains unchanged
        pass

# Initialize the game with two players
players = (Player("X", "blue"), Player("O", "green"))
game = TicTacToeGame(players)

# Define the game board size
board_size = 3

    # Other game logic methods remain unchanged

# Create a state for the board, which will hold the moves
board_state = [[" " for _ in range(board_size)] for _ in range(board_size)]

# Define actions for player moves and resetting the game
def play(row, col):
    move = Move(row, col, game.current_player.label)
    if game.is_valid_move(move):
        game.process_move(move)
        board_state[row][col] = game.current_player.label
        if game.has_winner():
            tp.notify(f"Player {game.current_player.label} wins!", category="success")
        elif game.is_tied():
            tp.notify("The game is tied!", category="info")
        game.toggle_player()
    else:
        tp.notify("Invalid move. Try again.", category="error")

def reset_game():
    global game
    game.reset_game()
    for row in range(board_size):
        for col in range(board_size):
            board_state[row][col] = " "
    tp.notify("Game reset. Ready to play!", category="info")

# Define the GUI layout
md = """
<|{display_message}|label|>

<|{board_state}|table|editable=False|>

<|Reset Game|button|on_action=reset_game|>
"""

# Initialize the GUI with the layout
gui = tp.Gui(md)

# Bind the game state and actions to the GUI
gui.display_message = "Ready to play!"
gui.board_state = board_state

# Add actions for each cell
for row in range(board_size):
    for col in range(board_size):
        _Gui_on_action(f"board_state.{row}.{col}", lambda row=row, col=col: play(row, col))

gui.run(title="Tic-Tac-Toe Game")