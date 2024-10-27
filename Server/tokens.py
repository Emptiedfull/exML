from collections import deque 
import threading
import secrets,string
from emailHandler import sendEmail
import requests


token_queue = deque()
queue_lock = threading.Lock()

link = "http://localhost:5000"

token_timer = None

def gen_token(length=16):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def remove_top():
   
    global token_timer
    with queue_lock:
        if token_queue:
            token_queue.popleft()
            requests.post("http://127.0.0.1:5000/token-expire")
            print("Removed top token from queue")
            token_timer = None
            if token_queue:
                start_top_token_timer()

def start_top_token_timer():
    global token_timer
    token_timer = threading.Timer(20,remove_top)
    token_timer.start()

def add_entry(email):
    

    with queue_lock:
        for entry in token_queue:
            if entry["email"] == email:
                return "failed"
        else:
            token = gen_token()
            mail_status  = sendEmail(token,email)
            if mail_status == "invalid email":
                return "invalid email"
                
            token_queue.append({"token":token,"email":email})
            
            
            print("Added token to queue:",token)

            if len(token_queue) == 1:
                start_top_token_timer()
           
            return "success"



def get_entry(token):
    with queue_lock:
        for entry in token_queue:
            if entry["token"] == token:
                position = token_queue.index(entry)
                if position == 0:
                    return {"position":position,"role":"player"}
                else:
                    return {"position":position,"role":"observer"}
        return None
    

def remove_entry(token):
   
    with queue_lock:
        try:
            for entry in token_queue:
                if entry["token"] == token:
                    token_queue.remove(entry)
                    print("Removed token from queue:",token)
                    return
           
        except ValueError:
            print('error')
            pass
        return None
    
def get_all():
    with queue_lock:
        return list(token_queue)
    
