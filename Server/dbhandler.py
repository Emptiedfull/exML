
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import env
import secrets
import string


var = env.parse("var.txt")
uri = var['uri']

def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def add_participant(name,school_code):
    db = client['game']
    col = db['participants']
    col.insert_one({'name': name, 'status':'inactive', 'password':school_code})

def get_participants():
    db = client['game']
    col = db['participants']
    return list(col.find())

def get_participant(name):
    db = client['game']
    col = db['participants']
    return col.find_one({'name':name})

def validate_participant(name,password):
    db = client['game']
    col = db['participants']
    participant = col.find_one({'name':name,'password':password})
    if participant:
        col.update_one({'name':name},{'$set':{'status':'active'}})

        return col.find_one({'name':name,'password':password})
    else:
        return None
    
def end_game(name):
    db = client['game']
    col = db['participants']
    col.update_one({'name':name},{'$set':{'status':'inactive'}})



