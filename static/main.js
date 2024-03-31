$(document).ready(function() {
    $('.cell').click(function() {
        var id = $(this).attr('id');
        var coordinates = id.split('-').slice(1).map(Number);
        var row = coordinates[0];
        var col = coordinates[1];
        
        makeMove(row, col);
    });
});

function makeMove(row, col) {
    fetch('/make_move', {
        method: 'POST',
        body: JSON.stringify({row: row, col: col}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var cellId = `#cell-${row}-${col}`;
            $(cellId).text(data.current_player);
            $('#game-status').text(`${data.current_player}'s turn`);
        } else if (data.winner) {
            $('#game-status').text(`Player ${data.winner} won!`);
            disableClicks();
        } else if (data.tied) {
            $('#game-status').text('Tied game!');
            disableClicks();
        }
    });
}

function disableClicks() {
    $('.cell').off('click');
}
