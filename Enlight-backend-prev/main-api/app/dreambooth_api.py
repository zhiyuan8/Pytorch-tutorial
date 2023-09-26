from app import app
from flask import request, json
import time, datetime
import os
import base64
import requests
from threading import Thread
from app.mongo_client import MongoClient, parameters
from app.redis_client import RedisClient
from app.prompt_generation_api import generate_prompt
import numpy as np
from PIL import Image
from io import BytesIO

TRAIN_API_URL = parameters.get('TRAIN_API_URL')
INFERENCE_API_URL = parameters.get('INFERENCE_API_URL')
REMBG_URL = parameters.get('REMBG_URL')
if not TRAIN_API_URL or not INFERENCE_API_URL:
    raise ValueError("Please set the environment variables TRAIN_API and INFERENCE_API")

client = MongoClient().client
db = MongoClient().db
redis_client = RedisClient()
import logging
logging.basicConfig(level=logging.DEBUG)


# Check if a image already has white background
def check_if_whitebg_base64(img_str, threshold=0.6):
    base64_decoded = base64.b64decode(img_str)
    image = Image.open(BytesIO(base64_decoded))
    image_np = np.array(image)[..., 0:3]
    H, W = image_np.shape[:2]

    # number of white pixels in top, bottom, left, right
    top = (image_np[0, :] == 255.).sum() / 3.
    bottom = (image_np[-1, :] == 255.).sum() / 3.
    left = (image_np[:, 0] == 255.).sum() / 3.
    right = (image_np[:, -1] == 255.).sum() / 3.

    return (top + bottom + left + right) / (H * 2 + W * 2) > threshold

# Helpful function to remove the background of an image
def remove_bg_base64string(http_url, string_with_bg):
    
    if check_if_whitebg_base64(string_with_bg):
        return string_with_bg
    
    payload = json.dumps({
        "input_image": string_with_bg,
        "model": "u2net"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", http_url, headers=headers, data=payload)
    string_no_bg = response.json()['output_image']
    return string_no_bg


# API for getting the generating progress
@app.route('/get-generating-progress', methods=['GET'])
def get_generate_progress():
    username = request.args['username']
    projectid = request.args['projectid']
    promptid = request.args['promptid']
    api_run_name = f"generating-{username}-{projectid}-{promptid}"
    collection = db["progress"]
    project_info = collection.find_one({'api_run_name': api_run_name})
    if project_info is None:
        progress_percentage = 0
    else:
        progress_percentage = project_info.get('inference', 0)
    progress_percentage = int(progress_percentage * 100)
    return {"progress": progress_percentage}



# This API resets the progress of generating to 0. It will be called by the client when the user starts a new
# generation process.
@app.route('/reset-generating-progress', methods=['GET'])
def reset_generating_progress():
    username = request.args['username']
    projectid = request.args['projectid']
    promptid = request.args['promptid']
    api_run_name = f"generating-{username}-{projectid}-{promptid}"
    collection = db["progress"]
    collection.update_one({'api_run_name': api_run_name}, 
                            {'$set': {'inference': 0}})
    return {"message":"success"}



# API for getting the training progress
@app.route('/get-training-progress', methods=['GET'])
def get_train_progress():
    username = request.args['username']
    projectid = request.args['projectid']
    api_run_name = f"training-{username}-{projectid}"
    collection = db["progress"]
    project_info = collection.find_one({'api_run_name': api_run_name})
    if project_info is None:
        progress_percentage = 0
    else:
        progress_percentage = project_info.get('train', 0)
    progress_percentage = int(progress_percentage * 100)
    return {"progress": progress_percentage}


# This API is the main training API. It will first upload the training data to the database, then call the training API
# in the docker container to start training. After the training is done, it will update the database again
# to indicate that the training is done.
@app.route('/train', methods=['GET'])
def train_dreambooth():
    username = request.args['username']
    project_id = request.args["project_id"]
    category_name = request.args['category_name']
    
    
    collection = db["projects"]

    # set training started
    collection.update_one({'username': username, 'project_id': project_id},
                            {'$set': {'training_started': True,
                                    'category_name': category_name}},
                            upsert=True)

    # create model card name for this finetuned model
    model_name = f"{username}-{project_id}"

    collection.update_one({'username': username, 'project_id': project_id}, 
                            {'$set': {
                                        'model_name': model_name,
                                        'category_name': category_name}
                            },
                            upsert=True)
    
    source_coll = db["source_images"]
    projection = {"image_data": False}
    sources = source_coll.find({'username': username, 
                                'project_id': project_id},
                                projection=projection)
    encoded_image_list_bg = []
    for s in sources:
        filename = s['filename']
        encoded_image_list_bg.append(redis_client.get_image(filename=filename,
                                                         collection='source_images'))
    
    encoded_image_list = [
        remove_bg_base64string(REMBG_URL, encoded_image) for \
            encoded_image in encoded_image_list_bg
    ]
    
    # train the model by calling the api
    dreambooth_training_api_url = TRAIN_API_URL
    
    request_params = {
        "MODEL_NAME": "stabilityai/stable-diffusion-2-1",
        "IMAGE_LIST": encoded_image_list,
        "OUTPUT_DIR": model_name,
        "INSTANCE_PROMPT": "a photo of a sks " + category_name,
        "MAX_TRAINING_STEPS": 400,
        "LR": 2e-6,
        "TRAIN_BATCH_SIZE": 1,
        "API_RUN_NAME": f"training-{username}-{project_id}"
    }

    _ = requests.post(dreambooth_training_api_url, json=request_params)
    logging.info("Training finished!")

    collection.update_one({'username': username, 'project_id': project_id},
                            {'$set': {'training_ended': True}},
                            upsert=True)

    # We use 101% to indicate that the training is really done
    collection_progress = db["progress"]
    collection_progress.update_one({'api_run_name': f"training-{username}-{project_id}"},
                                    {'$set': {'train': 1.01}},
                                    upsert=True)

    # suggested_prompts = generate_prompt(query=category_name)
    # # add the suggested prompts to the database
    # collection = db["projects"]
    # collection.update_one({'username': username, 'project_id': project_id},
    #                     {'$set': {'suggested_prompt_counter': len(suggested_prompts)}},
    #                     upsert=True)
    # for i, prompt in enumerate(suggested_prompts):
    #     collection.update_one({'username': username, 'project_id': project_id},
    #                         {'$set': {f'suggested_prompt_{i}': prompt}},
    #                         upsert=True)

    return {"message":"success"}


@app.route('/suggest-prompt', methods=['GET'])
def get_suggested_prompt():
    username = request.args['username']
    project_id = request.args["project_id"]
    collection = db["projects"]
    category_name = collection.find_one({'username': username, 'project_id': project_id})['category_name']
    # randomize a number between 0 and suggested_prompt_counter
    import random
    random_index = random.randint(0, 10-1)
    prompt_list = [
        " on a city sidewalk, with tall buildings in the background, high resolution, photographic style, product photo, 8k, soft shadows.",
        " in the snow, high resolution, photographic style, 8k, product photo, soft shadows.",
        " on a wooden dock, with a lake or river in the background, high resolution, photographic style, soft shadows."
        " in a spa setting, surrounded by candles and rose petals, high resolution, photographic style, 8k, product photo, soft shadows.",
        " in a garden setting, surrounded by lush greenery and flowers, high resolution, photographic style, 8k, product photo, soft shadows.",
        " in a bedroom setting, surrounded by pillows and other bedroom essentials, high resolution, photographic style, 8k, product photo, soft shadows.",
        " in a park, surrounded by lush greenery and natural landscapes, high resolution, photographic style, 8k, product photo, soft shadows.",
        " in a forest, surrounded by tall trees and natural landscapes, high resolution, photographic style, 8k, product photo, soft shadows.",
        " on a stage, with a podium and music notes in the background to depict a school performance or auditorium, 8k, product photo, soft shadows.",
        " on a wooden table with pumpkins and fall foliage in the background, high resolution, photographic style, real photo, photorealistic, 8k, product photo, soft shadows."
    ]
    suggested_prompt = f"A photo of a {category_name}" + prompt_list[random_index]
    return {"prompt": suggested_prompt}


# This API is the main generating API. It will first upload the generating data to the database, do some necessary
# preprocessing (e.g., changing the prompt to include sks), then call the generating API in the docker container to
# start generating. When the generating is done, it will upload the generated images to the database.
@app.route('/generate', methods=['GET'])
def generate_dreambooth():
    username = request.args['username']
    project_id = request.args["project_id"]
    prompt_id = request.args["prompt_id"]
    num_generation = int(request.args['num_images_to_generate'])

    prompt_coll = db["prompts"]
    prompt_info = prompt_coll.find_one({'username': username,
                                        'project_id': project_id,
                                        'prompt_id': prompt_id})
    prompt = prompt_info['prompt_text']
    project_info = db["projects"].find_one({'username':username, 'project_id': project_id})
    category_name = project_info['category_name']
    model_name = project_info['model_name']
    prompt_new = prompt.replace(category_name, "sks " + category_name)
    prompt_coll.update_one({'username': username, 'project_id': project_id, 'prompt_id': prompt_id},
                            {'$set': {
                                "is_button_disabled": True,
                                "before_generation": False,
                            }}, upsert=True)

    # every time we generate, we need to create a new name for this api run, used for tracking progress
    api_run_name = f'generating-{username}-{project_id}-{prompt_id}'
    collection_progress = db["progress"]
    collection_progress.update_one({'api_run_name': api_run_name},
                                    {'$set': {'inference': 0}}, upsert=True)
    
    
    dreambooth_generation_api_url = INFERENCE_API_URL
    request_params = {
        "prompt": prompt_new,
        "model_id": model_name,
        "num_image": num_generation,
        "api_run_name": api_run_name
    }

    response = requests.post(dreambooth_generation_api_url, json=request_params)

    generated_images = response.json()['images']
    
    generated_coll = db["generated_images"]
    # upload generated images to the database
    for generated_image_string in generated_images:
        generated_coll.insert_one({'username': username,
                                    'project_id': project_id,
                                    'prompt_id': prompt_id,
                                    'filename': f"{time.time()}-{username}.png",
                                    'image_data': generated_image_string,
                                    'uploadDate': datetime.datetime.utcnow(),
                                    'bookmarked': False})
        
    prompt_coll.update_one({'username': username, 'project_id': project_id,
                            'prompt_id': prompt_id},
                            {'$set': {'is_button_disabled': False}})

    logging.info(f"Generation finished for {username} {project_id} {prompt_id}")
    # We use 101% to indicate that the generation is really done
    # including uploading the images to the database
    collection_progress.update_one({'api_run_name': api_run_name},
                                    {'$set': {'inference': 1.01}}, upsert=True)

    return {"message":"success"}
