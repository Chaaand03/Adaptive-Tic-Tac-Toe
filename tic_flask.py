from flask import Flask, render_template, request, jsonify
from Game_logic import TicTacToeGame, Move, Player
from question_utils import get_question

app = Flask(__name__)
game = TicTacToeGame()
parsed_data = None
correct_answer = 3

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_mcq_question', methods=['POST'])
def get_mcq_question():
    data = {}
    # data = get_question(parsed_data,correct_answer)
    data["question"] = "question"
    options = ["option1","option2","option3","option4"]
    data["options"] = options
    
    # Retrieve the question and options from the request data
    question = data['question']
    options = data['options']


    # Return the question and options in the response
    return jsonify({'question': question, 'options': options})

@app.route('/submit_mcq_answer', methods=['POST'])
def submit_mcq_answer():
    data = request.json
    row = data['row']
    col = data['col']
    answer = data['answer']

    # Dummy logic to check the answer (replace with your actual logic)
    correct_answer = "Paris"
    if answer == correct_answer:
        return jsonify({'correct': True})
    else:
        return jsonify({'correct': False})
    
@app.route('/tic-tac-toe')
def tic_tac_toe():
    return render_template('tic-tac-toe.html')    

if __name__ == "__main__":
    app.run(debug=True)
