from app import app
from flask import ( request, 
                   make_response, 
                   jsonify,
                   render_template, 
                   send_from_directory )
import time
from app.mongo_client import MongoClient
from app.redis_client import RedisClient
from datetime import datetime
import requests
import base64
import ipdb
import os

client = MongoClient().client
db = MongoClient().db
redis_client = RedisClient()


# upload the source image to the source image database.
@app.route('/upload-source-image', methods=['POST'])
def upload_source_image():
    username = request.args['username']
    project_id = request.args["project_id"]
    image_name = f"{time.time()}-{username}.png"
    collection = db["source_images"]
    f = request.files['file']
    base64_string = base64.b64encode(f.read()).decode('utf-8')
    collection.insert_one({"username": username,
                           "project_id": project_id,
                           "filename": image_name,
                           "image_data": base64_string,
                           'uploadDate': datetime.utcnow()})
    return {"message": "success",
            "image_name": image_name}


# delete the source image from the source image database.
@app.route('/delete-source-image', methods=['GET'])
def delete_source_image():
    username = request.args['username']
    project_id = request.args["project_id"]
    image_name = request.args["image_name"]
    collection = db["source_images"]
    collection.delete_one({"username": username,
                            "project_id": project_id,
                            "filename": image_name})
    return {"message": "success",
            "image_name": image_name}


# upload the generated image to the generated image database
@app.route('/upload-generated-image', methods=['POST'])
def upload_generated_image():
    username = request.args['username']
    project_id = request.args["project_id"]
    prompt_id = request.args["prompt_id"]
    image_name = f"{time.time()}-{username}.png"
    collection = db["generated_images"]
    f = request.files['file']
    base64_string = base64.b64encode(f.read()).decode('utf-8')
    collection.insert_one({"username": username,
                           "project_id": project_id,
                           "prompt_id": prompt_id,
                           "filename": image_name,
                           "image_data": base64_string,
                           "bookmarked": False,
                           "uploadDate": datetime.utcnow()})
    return {"message": "success"}


# Get all source images according to the username and project id.
# return a list of filenames that sorted by upload data.
@app.route('/get-source-image', methods=['GET'])
def get_source_image():
    username = request.args['username']
    project_id = request.args['project_id']
    collection = db["source_images"]
    projection = {'image_data': False}
    res = sorted((collection.find({'username': username, 
                                   'project_id': str(project_id)},
                                  projection = projection)),
                 key=lambda x: x['uploadDate'], reverse=False)
    return {'file_names': [file['filename'] for file in res]}


# Get the source image data based on the image name
@app.route('/get-source-image-data', methods=['GET'])
def get_source_image_data():
    image_name = request.args['image_name']
    res = redis_client.get_image(image_name, collection='source_images')
    return {'image_data': res}


# Get the low resolution source image data based on the image name
@app.route('/get-source-image-data-low-res', methods=['GET'])
def get_source_image_data_low_res():
    image_name = request.args['image_name']
    res = redis_client.get_image(image_name, collection='source_images', low_res=True)
    return {'image_data': res}


# Get all generated images according to the username, project id and prompt id
@app.route('/get-generated-image', methods=['GET'])
def get_generated_image():
    username = request.args['username']
    project_id = request.args['project_id']
    prompt_id = request.args['prompt_id']
    collection = db["generated_images"]
    res = sorted((collection.find({'username': username,
                                   'project_id': project_id,
                                   'prompt_id': prompt_id},
                                   projection={'image_data': False})),
                 key=lambda x: x['uploadDate'], reverse=True)
    ret = {'generated_images_data': [{'file_name': file['filename'],
                                       'is_bookmarked': file['bookmarked'],
                                      } for file in res]}
    return ret


# Get the generated image data based on the image name
@app.route('/get-generated-image-data', methods=['GET'])
def get_generated_image_data():
    image_name = request.args['image_name']
    res = redis_client.get_image(image_name)
    return {'image_data': res}


# Get a low resolution image data based on the image name
@app.route('/get-generated-image-data-low-res', methods=['GET'])
def get_generated_image_data_low_res():
    image_name = request.args['image_name']
    res = redis_client.get_image(image_name, low_res=True)
    return {'image_data': res}
