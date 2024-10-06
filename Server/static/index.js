var socket = io();

var player = document.getElementById('player-token')
var ghost = document.getElementById('ghost-token')

var player_dock = document.getElementById('player-dock')
var ghost_dock = document.getElementById('ghost-dock')

var gameover = document.getElementById('gameover')

document.addEventListener('DOMContentLoaded', function() {
    reset_button = document.getElementById('reset')
    reset_button.addEventListener('click',reset)



    var part_coll = document.getElementById('part-coll')
    var part_content = document.getElementById('part-content')

    part_coll.addEventListener('click',()=>{

        if (part_content.style.display === 'block'){
            part_content.style.display = 'none'
            part_content.style.maxHeight = 0
         }else{
            part_content.style.display = 'block'
            part_content.style.maxHeight = part_content.scrollHeight + 'px'
         }
    })

    var moves_coll = document.getElementById('moves-coll')
    var moves_content = document.getElementById('moves-content')

    moves_coll.addEventListener('click',()=>{
        if (moves_content.style.display === 'block'){
            moves_content.style.display = 'none'
            moves_content.style.maxHeight = 0
         }else{
            moves_content.style.display = 'block'
            moves_content.style.maxHeight = moves_content.scrollHeight + 'px'
         }
    })

    console.log(part_coll,part_content)
})
socket.on('connect', function() {
            console.log('Connected to server');
        });

socket.on('board',(board)=>{
    
    drawBoard(board[0]);
    show_points(board[1])
})

socket.on('player-connected',(name)=>{
    player.innerHTML = name
})
socket.on('ghost-connected',(name)=>{
    ghost.innerHTML = name
})

socket.on('playerdocked',()=>{
    player_dock.innerHTML = 'Docked'
})
socket.on('ghostdocked',()=>{
    ghost_dock.innerHTML = 'Docked'
})
socket.on('undock',()=>{
    player_dock.innerHTML = ''
    ghost_dock.innerHTML = ''
})

socket.on('token',(token)=>{
    var player_token = token[0]
    var ghost_token = token[1]
    
    player.innerHTML = player_token
    ghost.innerHTML = ghost_token
    
})

socket.on('game-over',({winner,timestamps})=>{

    winnerdisplay = document.getElementById('winner')

    gameover.style.opacity = 1
    document.querySelector('.gamearea').classList.add('overlay-active');
    winnerdisplay.style.opacity = 'nononon'
    if  (winner == 'player'){
        winnerdisplay.innerHTML = 'Player Wins'
    }else{
        winnerdisplay.innerHTML = 'Ghost Wins'
    }

})



const show_points = (points) => {
    var point = document.getElementById('player-points')
    var gameover_points = document.getElementById('score')
    point.innerHTML = points
    gameover_points.innerHTML = points
}

const reset = () => {
    socket.emit('reset')
    location.reload()

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


    var CellSize = 14;
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






