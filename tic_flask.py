import os
from flask import Flask, render_template, request, jsonify
from Game_logic import TicTacToeGame, Move, Player
from pdf_parser import parse_pdf_questions

app = Flask(__name__)
game = TicTacToeGame()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tic-tac-toe')
def tic_tac_toe():
    return render_template('tic-tac-toe.html')

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # filename = file.filename
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(file_path)
        # print('File saved:', file_path)
        parse_pdf_questions(file)
        # Process the file here as needed
        return 'File uploaded successfully'
    

if __name__ == "__main__":
    app.run(debug=True)
