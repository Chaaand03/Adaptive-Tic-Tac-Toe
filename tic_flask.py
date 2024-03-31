from flask import Flask, render_template, request, jsonify
from Game_logic import TicTacToeGame, Move, Player

app = Flask(__name__)
game = TicTacToeGame()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row = data['row']
    col = data['col']
    move = Move(row=row, col=col, label=game.current_player.label)
    if game.is_valid_move(move):
        game.process_move(move)
        if game.has_winner():
            return jsonify({'winner': game.current_player.label})
        elif game.is_tied():
            return jsonify({'tied': True})
        else:
            game.toggle_player()
            return jsonify({'success': True, 'current_player': game.current_player.label})
    else:
        return jsonify({'success': False})


if __name__ == "__main__":
    app.run(debug=True)
