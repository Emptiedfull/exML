var socket = io();

document.addEventListener('DOMContentLoaded', function() {
    reset_button = document.getElementById('reset')
    reset_button.addEventListener('click',reset)
})
socket.on('connect', function() {
            console.log('Connected to server');
        });

socket.on('board',(board)=>{
    
    drawBoard(board[0]);
    show_points(board[1])
})
socket.on('game-over',()=>{
    alert('Game Over')
    location.reload();

})

const show_points = (points) => {
    var point = document.getElementById('player-points')
    point.innerHTML = points
}

const reset = () => {
    socket.emit('reset')

}

function setCanvasDimensions(x,y) {
    var canvas = document.getElementsByClassName('canvas-layer');
    for (var i = 0; i < canvas.length; i++) {
        canvas[i].width = x;
        canvas[i].height = y;
    }
}

function drawBoard(board){
    var wallsCv = document.getElementById('walls');
    var wallsCtx = wallsCv.getContext('2d');
    var BackgroundCv = document.getElementById('background');
    var BackgroundCtx = BackgroundCv.getContext('2d');
    var foregroundCv = document.getElementById('foreground')
    var foregroundCtx = foregroundCv.getContext('2d');


    var CellSize = 15;
    var x = board[0].length*CellSize
    var y = board.length*CellSize
    setCanvasDimensions(x,y)

    BackgroundCtx.clearRect(0, 0, x, y);
    wallsCtx.clearRect(0, 0, x, y);
    foregroundCtx.clearRect(0, 0, x, y);

    for (var row=0;row<board.length;row++){
        for (var col=0;col<board[0].length;col++){

            try{
                cell = board[row][col]
            }catch{
                console.log(row,col)
                cell = board[row][col]
               
                continue
            }
            
            if (cell == "#"){
                wallsCtx.fillStyle = 'black';
                wallsCtx.fillRect(col*CellSize,row*CellSize,CellSize,CellSize);
            }
         

            if (cell == "."){
                foregroundCtx.fillStyle = 'orange';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/6);
            }
            if (cell == "p"){
                foregroundCtx.fillStyle = 'yellow';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/3);
            }
            if (cell == "a"){
                foregroundCtx.fillStyle = 'purple';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/3);
            }
            if (cell == "b"){
                foregroundCtx.fillStyle = 'red';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/3);
            }
            if (cell == "c"){
                foregroundCtx.fillStyle = 'blue';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/3);
            }
            if (cell == "d"){
                foregroundCtx.fillStyle = 'green';
                drawCircle(foregroundCtx,col*CellSize+CellSize/2,row*CellSize+CellSize/2,CellSize/3);
            }
        }
    }
}

function drawRoundedRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
    ctx.fill();
}
function drawCircle(ctx, x, y, radius) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.closePath();
    ctx.fill();
}