import flask
from Game import Player,Board,Ghost
import flask_socketio
import os

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

player_move_docked = False
ghost_move_docked = False

board = Board()



positions = board.get_positions()


player = Player(positions[0])
ghost1 = Ghost(positions[1],"a")
ghost2 = Ghost(positions[2],"b")
ghost3 = Ghost(positions[3],"c")
ghost4 = Ghost(positions[4],"d")

ghosts = [ghost1,ghost2,ghost3,ghost4]


@socketio.on('reset')
def reset():
    global player,ghost1,ghost2,ghost3,ghost4,ghosts,board
    board = Board()
    positions = board.get_positions()
    player = Player(positions[0])
    ghost1 = Ghost(positions[1],"a")
    ghost2 = Ghost(positions[2],"b")
    ghost3 = Ghost(positions[3],"c")
    ghost4 = Ghost(positions[4],"d")
    ghosts = [ghost1,ghost2,ghost3,ghost4]
    socketio.emit('board', [board.get_board(),player.points])


def move_ghost(ghost,move,board):
    if move[0] == 1:
        ghost.move(board,"up")
    if move[1] == 1:
        ghost.move(board,"down")
    if move[2] == 1:
        ghost.move(board,"left")
    if move[3] == 1:
        
        ghost.move(board,"right")

def move_ghosts(ghosts,moves):
    for i in range(len(moves)):
        move_ghost(ghosts[i],moves[i],board)

def move_player(player,move):

    print(move)

    if move[0] == 1:
        state = player.move(board,"up")

       
    elif move[1] == 1:
        state = player.move(board,"down")
        
    elif move[2] == 1:
        state = player.move(board,"left")
       
    elif move[3] == 1:
        state = player.move(board,"right")
        
    else:
        status = "invalid move"
    if state == "death":
        status = "death"
    else:
        status = "success"
        
    return status




def handlemove(obj,move):
    global player_move_docked,ghost_move_docked,ghost_move,player_move

    if obj == "player":
        
        player_move_docked = True
        player_move = move
        print("docked")
        
    if obj == "ghost":
        ghost_move_docked = True
        ghost_move = move
        print("docked")
    
    if player_move_docked and ghost_move_docked:
        player_move_docked = False
        ghost_move_docked = False
        player_status  = move_player(player,player_move)
        status = move_ghosts(ghosts,ghost_move)
        
        socketio.emit('board', [board.get_board(),player.points])
        if player_status == "death":
            socketio.emit('game-over')
     
        

@app.route('/')
def index():

    return flask.render_template('index.html')


@app.route('/move/player', methods=['POST'])
def player_move():

    status  = handlemove("player",flask.request.get_json())
    return "Sucess"

@app.route('/move/ghost', methods=['POST'])
def ghost_move():
   
    move = flask.request.get_json()
    if isinstance(move,list):
        handlemove("ghost",move)
        
        return "Success"
    else:
        return flask.jsonify({"error":"Invalid move"})
   
@socketio.on('connect')
def handle_connect():
    print('Client connected')
  
    socketio.emit('board', [board.get_board(),player.points])
    
   
  

if __name__ == '__main__':

    extra_files = [
        os.path.join(os.getcwd(), 'static', 'index.js'),
        os.path.join(os.getcwd(), 'templates', 'index.html')
    ]
    socketio.run(app, debug=True, extra_files=extra_files) 

