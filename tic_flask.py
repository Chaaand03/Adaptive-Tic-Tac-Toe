from multiprocessing.connection import answer_challenge
import os
from flask import Flask, render_template, request, jsonify
from requests import session
from Game_logic import TicTacToeGame, Move, Player
from pdf_parser import parse_pdf_questions
from question_utils import get_question


app = Flask(__name__)
game = TicTacToeGame()
parsed_data = None
correct_count = 0
correct_answer = None
filename = None

@app.route('/')
def index():
    print("inside index function")
    return render_template('index.html')


@app.route('/get_mcq_question', methods=['POST'])
def get_mcq_question():
    global correct_answer
    row = request.json["row"]
    column = request.json["col"]
    data = {}
    data = get_question(parsed_data,correct_count)
    # data["question"] = "question"
    # options = ["option1","option2","option3","option4"]
    # data["options"] = options
    
    # Retrieve the question and options from the request data
    question = data['question']
    print(question)
    options = data['options']
    correct_answer = data['ans']


    # Return the question and options in the response
    return jsonify({'question': question, 'options': options,'ans': correct_answer,'row': row,'column': column})

@app.route('/submit_mcq_answer', methods=['POST'])
def submit_mcq_answer():
    data = request.json
    print(data)
    row = data['row']
    col = data['col']
    answer = data['answer']
    print(correct_answer)
    if answer == correct_answer:
        return jsonify({'correct': True,'row':row,'col':col})
    else:
        return jsonify({'correct': False})

@app.route('/upload', methods=['POST'])
def upload_file():
    global parsed_data
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = file.filename
        filename = filename[:-4] if filename.endswith('.pdf') else filename
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(file_path)
        # print('File saved:', file_path)
        parsed_data = parse_pdf_questions(file)
        # Process the file here as needed
        return render_template('tic-tac-toe.html', filename=filename)
    else:
        return "File couldn't be parsed"
        
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
    

    
@app.route('/tic-tac-toe')
def tic_tac_toe():
    global filename
    return render_template('tic-tac-toe.html', filename=filename)    

if __name__ == "__main__":
    app.run(debug=True)
