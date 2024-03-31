$(document).ready(function() {
    $('.cell').click(function() {
        console.log("tick openMCQpopup")
        var id = $(this).attr('id');
        var coordinates = id.split('-').slice(1).map(Number);
        var row = coordinates[0];
        var col = coordinates[1];
        
        // Open pop-up with MCQ
        openMCQPopup(row, col);
    });
});

function openMCQPopup(row, col) {
    //Fetch MCQ question from the server
    fetch('/get_mcq_question', {
        method: 'POST',
        body: JSON.stringify({row: row, col: col}),
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
            $('#optionA').text(optionA);
            $('#optionB').text(optionB);
            $('#optionC').text(optionC);
            $('#optionD').text(optionD);
            $('#mcq-popup').show();
        } else {
            console.error("Error: No MCQ question received from server.");
        }
    });
}

// Function to handle MCQ answer submission
function submitMCQAnswer() {
    var selectedOption = $("input[name='mcq-option']:checked").val();
    var row = $('#mcq-popup').data('row');
    var col = $('#mcq-popup').data('col');
    
    // Send MCQ answer to the server
    fetch('/submit_mcq_answer', {
        method: 'POST',
        body: JSON.stringify({row: row, col: col, answer: selectedOption}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.correct) {
            // Display success message or perform desired action
            alert("Correct Answer!");
        } else {
            // Display failure message or perform desired action
            alert("Incorrect Answer. Try again!");
        }
    });
}

// Function to close the MCQ pop-up
function closeMCQPopup() {
    $('#mcq-popup').hide();
}


function disableClicks() {
    $('.cell').off('click');
}
