$(document).ready(function() {
    $('.cell').click(function() {
        console.log("tick openMCQpopup")
        var id = $(this).attr('id');
        var coordinates = id.split('-').slice(1).map(Number);
        var row = coordinates[0];
        var col = coordinates[1];
        
        // Open pop-up with MCQ
        openMCQPopup(row, col);
        makeMove(row, col);
    });
});

function openMCQPopup(row, col) {
    //Fetch MCQ question from the server
    fetch('/get_mcq_question', {
        method: 'POST',
        body: JSON.stringify({'row': row, 'col': col}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("open Mcq popup")
        if (data.question) {
            console.log("mcqPopUp")
            // Display MCQ question in a pop-up
            var question = data.question;
            var optionA = data.options[0];
            var optionB = data.options[1];
            var optionC = data.options[2];
            var optionD = data.options[3];
            
            // Show the MCQ pop-up
            $('#mcq-question').text(question);
            $('#labelA').text(optionA);
            $('#labelB').text(optionB);
            $('#labelC').text(optionC);
            $('#labelD').text(optionD);
            $('#optionA').val(optionA);
            $('#optionB').val(optionB);
            $('#optionC').val(optionC);
            $('#optionD').val(optionD);
            $('#mcq-popup').attr('data-row',data.row)
            $('#mcq-popup').attr('data-col',data.column)
            $('#mcq-popup').attr('data-ans',data.ans)
            console.log(data.ans)
            $('#mcq-popup').show();
        } else {
            console.error("Error: No MCQ question received from server.");
        }
    });
}

// Function to handle MCQ answer submission
function submitMCQAnswer() {
    var selectedOption = $("input[name='mcq-option']:checked").val();
    console.log(selectedOption)
    var row = $('#mcq-popup').data('row');
    var col = $('#mcq-popup').data('col');
    var correct_answer = $('#mcq-popup').data('ans');
    console.log(correct_answer)
    
    // Send MCQ answer to the server
    fetch('/submit_mcq_answer', {
        method: 'POST',
        body: JSON.stringify({'row': row, 'col': col, 'answer': selectedOption,'correct_answer': correct_answer}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.correct) {
            // Display success message or perform desired action
            alert("Correct Answer!");
            closeMCQPopup();
            makeMove(data.row, data.col);
        } else {
            // Display failure message or perform desired action
            alert("Incorrect Answer. Try again!");
        }
    });
}

function makeMove(row, col) {
    // Fetch data from server and update grid
    fetch('/make_move', {
        method: 'POST',
        body: JSON.stringify({'row': row, 'col': col}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Handle server response and update grid
        if (data.success) {
            var cellId = "#cell-" + row + "-" + col;
            $(cellId).text(data.current_player);
            $('#game-status').text(data.current_player + "'s turn");
        } else if (data.winner) {
            $('#game-status').text("Player " + data.winner + " won!");
            disableClicks(); // Disable further moves
        } else if (data.tied) {
            $('#game-status').text('Tied game!');
            disableClicks(); // Disable further moves
        } else {
            console.error("Unexpected response from server:", data);
        }
    })
    .catch(error => {
        console.error('Error making move:', error);
    });
}

// Function to disable further clicks on cells
function disableClicks() {
    $('.cell').off('click');
}
// Function to close the MCQ pop-up
function closeMCQPopup() {
    $('#mcq-popup').hide();
}


function disableClicks() {
    $('.cell').off('click');
}
