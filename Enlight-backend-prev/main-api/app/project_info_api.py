from app import app
from flask import request, jsonify
from app.mongo_client import MongoClient
import requests
from app.cloud_storage import remove_model
import os

client = MongoClient().client
db = MongoClient().db

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Get current project information based on the username, and project_id
@app.route('/get-project-init-state', methods=['GET'])
def get_project_init_state():
    username = request.args['username']
    project_id = request.args['project_id']
    collection = db["projects"]
    project_info = collection.find_one({'username': username,
                                        'project_id': project_id})
    if project_info is None: project_info = {}

    # get the list of prompt ids
    collection = db["prompts"]
    prompt_ids = collection.distinct('prompt_id', {'username': username,
                                                   'project_id': project_id})
    project_info['prompt_ids'] = prompt_ids

    # return the project information
    result = {
        'category_name': project_info.get('category_name', ''),
        'project_name': project_info.get('project_name', 'New Project'),
        'prompt_counter': project_info.get('prompt_counter', 0),
        'prompt_ids': project_info.get('prompt_ids', []),
        'training_started': project_info.get('training_started', False),
        'training_ended': project_info.get('training_ended', False)
    }
    return jsonify(result)


# Get the current prompt information based on the username, project_id and prompt_id
@app.route('/get-prompt-init-state', methods=['GET'])
def get_prompt_init_state():
    # passed params
    username = request.args['username']
    project_id = request.args['project_id']
    prompt_id = request.args['prompt_id']
    
    collection = db["prompts"]
    project_info = collection.find_one({'username': username,
                                        'project_id': str(project_id),
                                        'prompt_id': str(prompt_id)})
    if not project_info: project_info = {}

    result = {
        'prompt_text': project_info.get("prompt_text", ''),
        'is_button_disabled': project_info.get("is_button_disabled", False),
        'before_generation': project_info.get("before_generation", False)
    }

    return jsonify(result)


# Reset a certain project_id
# This will delete all the source images, prompts and progress
@app.route('/reset-project', methods=['GET'])
def reset_project():
    username = request.args['username']
    project_id = request.args['project_id']
    prompts_coll = db["prompts"]
    progress_coll = db["progress"]
    source_coll = db["source_images"]
    
    # delete the progress collection first
    project_info = prompts_coll.find({'username': username,
                                      'project_id': project_id})
    if not project_info: project_info = {}
    prompt_ids = [prompt['prompt_id'] for prompt in project_info]
    progress_coll.delete_many({'api_run_name': f"training-{username}-{project_id}"})
    try:
        for prompt_id in prompt_ids:
            progress_coll.delete_one({'api_run_name':
                                      f"generating-{username}-{project_id}-{prompt_id}"})
    except:
        pass
    
    # delete all source images
    source_coll.delete_many({'username': username,
                             'project_id': project_id})
    
    # delete all occurrence of documents in the prompts collection
    # matching username and project_id
    prompts_coll.delete_many({'username': username,
                              'project_id': project_id})
    return jsonify({'message': 'success'})


@app.route('/add-new-prompt', methods=['GET'])
def add_new_prompt():
    # passed parameters
    username = request.args['username']
    project_id = request.args['project_id']
    prompt = request.args['prompt']

    projects_coll = db["projects"]
    prompts_coll = db["prompts"]
    
    # update the projects coll
    try:
        prompt_counter = projects_coll.find_one({'username': username,
                                                 'project_id': project_id}).get('prompt_counter', 0)
        projects_coll.update_one({'username': username, 'project_id': project_id},
                                 {'$set': {'prompt_counter': prompt_counter + 1}},
                                 upsert=True)
    except:
        raise Exception("Invalid project id or username")
    
    # update the prompts coll
    prompt_id = prompt_counter
    prompts_coll.update_one({'username': username,
                             'project_id': project_id,
                             'prompt_id': str(prompt_id)},
                            {"$set": 
                                { 
                                 "prompt_text": prompt,
                                 'before_generation': True,
                                 'is_button_disabled': False
                                }
                            }, upsert=True)
    return jsonify({'message': 'success'})


@app.route('/delete-prompt', methods=['GET'])
def delete_prompt():
    username = request.args['username']
    project_id = request.args['project_id']
    prompt_id = request.args['prompt_id']

    collection = db["prompts"]
    
    collection.delete_one({'username': username,
                           'project_id': project_id,
                           'prompt_id': prompt_id})
    return jsonify({'message': 'success'})


# Given one username, return a list of all project ids.
@app.route('/get-project-list', methods=['GET'])
def get_project_list():
    username = request.args['username']

    collection = db['projects']
    project_info = list(collection.find({'username': username}))
    # If no project exists, create a new project
    if not project_info:
        url = f"http://localhost:8040/create-new-project?username={username}"
        res = requests.get(url)
        return jsonify({'project_list': [{
            'project_id': res.json()['new_project_id'],
            'project_name': res.json()['new_project_name']
        }]})
    else:
        return jsonify({'project_list': [{
            'project_id': project['project_id'],
            'project_name': project['project_name']
        } for project in project_info]})


@app.route('/create-new-project', methods=['GET'])
def create_new_project():
    username = request.args['username']
    collection = db["users"]
    user_info = collection.find_one({'username': username})
    if not user_info:
        collection.insert_one({'username': username, 'total_counter': 0})
    total_counter = user_info.get('total_counter', 0) if user_info else 0
    new_project_id = total_counter
    collection.update_one({'username': username},
                          {'$set': {'total_counter': str(int(total_counter)+1)}},
                          upsert=True)
    
    project_coll = db["projects"]
    project_coll.update_one({'username': username, 'project_id': str(new_project_id)},
                            {'$set': 
                                {
                                 'prompt_counter': 0,
                                 'project_name': 'New Project'
                                }
                            }, upsert=True)
    return jsonify({'new_project_id': str(new_project_id),
                    'new_project_name': 'New Project'})


# We delete the projects based on the username and project_id
# Note that we don't delete the generated images here! Since the images may 
# already be bookmarked by the users. And the useless images will be deleted by
# the TTL mechanism in the database.
@app.route('/delete-project', methods=['GET'])
def delete_project():
    username = request.args['username']
    project_id = request.args['project_id']
    
    projects_coll = db["projects"]
    prompts_coll = db["prompts"]
    progress_coll = db["progress"]
    source_coll = db["source_images"]
    
    # delete the progress collection first
    project_info = prompts_coll.find({'username': username,
                                      'project_id': project_id})
    if not project_info: project_info = {}
    prompt_ids = [prompt['prompt_id'] for prompt in project_info]
    progress_coll.delete_many({'api_run_name': f"training-{username}-{project_id}"})
    try:
        for prompt_id in prompt_ids:
            progress_coll.delete_one({'api_run_name':
                                      f"generating-{username}-{project_id}-{prompt_id}"})
    except:
        pass
    
    # delete all source images
    source_coll.delete_many({'username': username,
                             'project_id': project_id})
    
    # delete all occurrence of documents in the projects collection
    # matching username and project_id
    projects_coll.delete_many({'username': username,
                               'project_id': project_id})
    prompts_coll.delete_many({'username': username,
                              'project_id': project_id})
    
    # delete the model in the cloud storage
    remove_model(f"{username}-{project_id}", "modelids")
    return jsonify({'message': 'success'})


@app.route('/update-project-name', methods=['GET'])
def update_project_name():
    username = request.args['username']
    project_id = request.args['project_id']
    project_name = request.args['new_project_name']

    collection = db['projects']
    collection.update_one({'username': username, 'project_id': project_id},
                          {'$set': {'project_name': project_name}},
                          upsert=True)
    return jsonify({'message': 'success'})


# Alex TODO: Why do we need this?
# return the id of the first project of a specific user
@app.route('/get-first-project-id', methods=['GET'])
def get_first_project_id():
    username = request.args['username']

    collection = db["projects"]
    try:
        project_info = collection.find({'username': username})
        project_list = sorted(project_info, key=lambda x: int(x['project_id']))
        return jsonify({'project_id': project_list[0]['project_id']})
    except:
        raise Exception(f"{username} but no project")