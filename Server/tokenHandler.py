from flask import blueprints
import flask
from tokens import add_entry,remove_entry,get_entry,get_all


token_handler = blueprints.Blueprint('token_handler', __name__)

@token_handler.route('/add',methods=['POST'])
def add_token():
    email = flask.request.get_json()
    print(email.get('email'))
    if email == None:
        return flask.jsonify({"error":"Missing email"}),400
    status = add_entry(email.get('email'))
    if status == "failed":
        print("email in queue")
        return flask.jsonify({"error":"Email already in queue"}),400
    if status == "invalid email":
        return flask.jsonify({"error":"Invalid email"})
    print(status)
    return flask.jsonify({"status":status})

    
@token_handler.route('/')
def hi():
    return "hi"

@token_handler.route('/queue',methods=['GET'])
def queue():
    return flask.jsonify({"queue":get_all()})

@token_handler.route('/get',methods=['GET'])
def get():
   
    token = flask.request.args.get('token')
    print("haha",token)
    if token == None:
        return flask.jsonify({"error":"Missing token"}),400
    status = get_entry(token)
    if status == None:
        return flask.jsonify({"error":"Token not found"}),401
    return flask.jsonify({"status":status})

