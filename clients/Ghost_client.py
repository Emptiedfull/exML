import socketio
import time
import requests

link = "http://127.0.0.1:5000"


sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')


@sio.on('board')
def handle_server_message(data):
    board,points = data
    process(board,points)

def process(board,points):
    move = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #create model here
    send_move(move)

def send_move(move):
   url = f"{link}/move/ghost"
   payload = move
   headers = {'content-type': 'application/json'}
   response = requests.post(url, json=payload, headers=headers)
   print(response.text)


sio.connect(link)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting from server...")
    sio.disconnect()
    print("Disconnected. Exiting...")