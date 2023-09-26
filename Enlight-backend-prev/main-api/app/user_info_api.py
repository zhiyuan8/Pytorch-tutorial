from app import app
from flask import request, jsonify
from app.mongo_client import MongoClient

client = MongoClient().client
db = MongoClient().db

# This is to set various user information
# like the credit, email, name, etc.
# This is called when the user first logs in
@app.route('/init-user', methods=['GET'])
def init_user():
    username = request.args['username']
    collection = db["users"]
    collection.update_one(
                          {'username': username},
                          {'$set': {'username': username}},
                          upsert=True)
    return jsonify({'message': 'success'})


# return the mode preference
@app.route('/get-user-mode-preference', methods=['GET'])
def get_user_mode_preference():
    username = request.args['username']
    collection = db["users"]
    user_info = collection.find_one({'username': username})
    if user_info is None:
        return jsonify({'mode': 'dark'})
    return jsonify({'mode': user_info.get('mode', 'dark')})


# set the mode preference
@app.route('/set-mode', methods=['GET'])
def set_mode():
    username = request.args['username']
    mode = request.args['mode']
    collection = db["users"]
    collection.update_one(  
                          {'username': username},
                          {'$set': {'mode': mode}},
                        upsert=True)
    return jsonify({'message': 'success'})
