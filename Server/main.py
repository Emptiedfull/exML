import flask
from Game import Player, Board, Ghost
import flask_socketio
from flask_socketio import ConnectionRefusedError,disconnect
from flask import request
import os
import random
import string
import time

def write_tokens_to_file(player_token, ghost_token, filename='tokens.txt'):
    with open(filename, 'w') as file:
        file.write(f"Player Token: {player_token}\n")
        file.write(f"Ghost Token: {ghost_token}\n")


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


connected_clients = []
player_token = generate_random_string()
ghost_token = generate_random_string()
write_tokens_to_file(player_token, ghost_token)

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)



player_move_docked = False
ghost_move_docked = False

player_connected = False
ghost_connected = False

player_name = None
ghost_name = None

def initialize():
    global board, player, ghost1, ghost2, ghost3, ghost4, ghosts, player_token, ghost_token, player_connected, ghost_connected, player_name, ghost_name, player_move_docked, ghost_move_docked, positions, player, ghost1, ghost2, ghost3, ghost4, board,connected_clients

    player_move_docked = False
    ghost_move_docked = False

    player_connected = False
    ghost_connected = False

    player_name = None
    ghost_name = None
    board = Board()
    positions = board.get_positions()

    player = Player(positions[0])
    ghost1 = Ghost(positions[1], "a")
    ghost2 = Ghost(positions[2], "b")
    ghost3 = Ghost(positions[3], "c")
    ghost4 = Ghost(positions[4], "d")

    ghosts = [ghost1, ghost2, ghost3, ghost4]

    player_token = generate_random_string()
    ghost_token = generate_random_string()
    write_tokens_to_file(player_token, ghost_token)

    for id in connected_clients:
        disconnect(id)
    connected_clients = []

    
    
    

board = Board()
positions = board.get_positions()


player = Player(positions[0])
ghost1 = Ghost(positions[1],"a")
ghost2 = Ghost(positions[2],"b")
ghost3 = Ghost(positions[3],"c")
ghost4 = Ghost(positions[4],"d")

ghosts = [ghost1,ghost2,ghost3,ghost4]



@socketio.on('hi')
def handle_hi():
    print('hi')
 

@socketio.on('reset')
def reset():
   print('reset')
   initialize()


def move_ghost(ghost,move,board):
    if move.count(1) > 1:
        return

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

    if move.count(1) > 1:
        return

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
        socketio.emit('playerdocked')
        print("player move recieved")
      
        
    if obj == "ghost":
        ghost_move_docked = True
        ghost_move = move
        socketio.emit('ghostdocked')
        print("ghost move recieved")
    
    if player_move_docked and ghost_move_docked:
        timestamp = time.time()
        player_move_docked = False
        ghost_move_docked = False
        player_status  = move_player(player,player_move)
        status = move_ghosts(ghosts,ghost_move)
        socketio.emit('undock')
        socketio.emit('board', [board.get_board(),player.points])
        if player_status == "death":
            socketio.emit('game-over')
     


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/move/player', methods=['POST'])
def player_move():
    move = flask.request.get_json()
    auth = request.headers.get('Authorization')
    if auth:
        token = auth.split(' ')[1]
    else:
        return flask.jsonify({"error":"Missing Token"}), 401
    if token != player_token:
        return flask.jsonify({"error": "Unauthorized"}),403
    if not player_connected:
        return flask.jsonify({"error": "Player not connected"}),400
    handlemove("player", move)
    return flask.jsonify({"status": "success"})

@app.route('/move/ghost', methods=['POST'])
def ghost_move():
   
    move = flask.request.get_json()

    auth = request.headers.get('Authorization')
    if auth:
        token = auth.split(' ')[1]
    else:
        return flask.jsonify({"error":"Missing Token"}), 401
    if not isinstance(move, list):
        return flask.jsonify({"error": "Invalid move"}),400
    if token != ghost_token:
        return flask.jsonify({"error": "Unauthorized"}),403
    if not ghost_connected:
        return flask.jsonify({"error": "Ghost not connected"}),400
    
    handlemove("ghost", move)
    return flask.jsonify({"status": "success"})
   


def display():
    if player_connected:
        socketio.emit('player-connected',player_name)
    if ghost_connected:
        socketio.emit('ghost-connected',ghost_name)
    if player_move_docked:
        socketio.emit('playerdocked')
    if ghost_move_docked:
        socketio.emit('ghostdocked')


@socketio.on('connect')
def handle_connect():

    global player_connected,ghost_connected,player_name,ghost_name
    

    
   
    origin = request.headers.get('Referer')
    server =  'http://127.0.0.1:5000/'

    if origin and origin.startswith(server):
        id = request.sid
        socketio.emit('board', [board.get_board(), player.points], to=id)
        display()
        print('display connected')
    else:
        token = request.headers.get('Authorization').split(' ')[1]
        name = request.headers.get('Name')
      

        if token == player_token:
            if player_connected == True:
                print('player already connected,disconnecting')
                raise ConnectionRefusedError('player already connected')
            player_connected = True
            player_name = name
            socketio.emit('player-connected',name)
            connected_clients.append(request.sid)
            print('player connected')
        elif token == ghost_token:
            if ghost_connected == True:
                raise ConnectionRefusedError('ghost already connected')
            ghost_connected = True
            ghost_name = name
            socketio.emit('ghost-connected',name)
            connected_clients.append(request.sid)
            print('ghost connected')
        else:
            print('invalid token')
            raise ConnectionRefusedError('unauthorized')
        

    
   
    
   
  

if __name__ == '__main__':

    extra_files = [
        os.path.join(os.getcwd(), 'static', 'index.js'),
        os.path.join(os.getcwd(), 'templates', 'index.html')
    ]
    socketio.run(app, debug=True, extra_files=extra_files) 

