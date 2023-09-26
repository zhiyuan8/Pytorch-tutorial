from app import app
from flask import request, jsonify
from app.mongo_client import MongoClient
from app.redis_client import RedisClient
redis_client = RedisClient()

db = MongoClient().db

@app.route('/add-bookmark', methods=['GET'])
def add_bookmark():
    collection = db["generated_images"]
    filename = request.args['filename']
    collection.update_one({'filename': filename},
                            { 
                            '$set': {'bookmarked': True}
                            }
                        )
    return {"message": "success"}


@app.route('/remove-bookmark', methods=['GET'])
def remove_bookmark():
    collection = db["generated_images"]
    filename = request.args['filename']
    collection.update_one({
        'filename': filename
    },{
        '$set': {'bookmarked': False}
    })
    return {"message": "success"}
    

@app.route('/get-bookmarked-images', methods=['GET'])
def get_bookmarked_images():
    collection = db["generated_images"]
    username = request.args['username']
    projection = {'image_data': False}
    documents = collection.find({'username': username, 'bookmarked': True},
                                projection=projection)
    # sort the documents by upload date
    documents = sorted(documents, key=lambda x: x['uploadDate'], reverse=False)
    res = [{'filename': document['filename'],
            'username': document['username'],
            'project_id': document['project_id'],
            'prompt_id': document['prompt_id']} \
            for document in documents]
    return {"output": res}
    
    