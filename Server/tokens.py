from collections import deque 
import threading
import secrets,string

token_queue = deque()
queue_lock = threading.Lock()

def gen_token(length=16):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token

def add_entry(email):
    

    with queue_lock:
        for entry in token_queue:
            if entry["email"] == email:
                return "failed",400
        else:
            token = gen_token()
            token_queue.append({"token":token,"email":email})
            print("Added token to queue:",token)
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