import os
from google.cloud import storage
from zipfile import ZipFile, ZipInfo
from pathlib import Path
import io
import shutil
import time
import json
from pymongo import MongoClient
from collections import OrderedDict
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

dotenv_path = Path('main.env')
parameters = dotenv_values(dotenv_path=dotenv_path)

MONGO_URL = parameters['MONGO_URL']
MONGO_DB = parameters['MONGO_DB']
CACHE_SIZE = parameters['CACHE_SIZE']

mongo_client = MongoClient(MONGO_URL)

start = time.time()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "TrainData_Key.json"

storage_client = storage.Client()

class LogInfo:
    def __init__(self, client=mongo_client):
        self.client = client
        self.db = self.client[MONGO_DB]
        self.collection = self.db['progress']
    
    def update_train_progress(self, api_run_name, progress):
        self.collection.update_one({'api_run_name': api_run_name},
                                   {'$set': {'train': progress}},
                                   upsert=True)
    
    def update_inference_progress(self, api_run_name, progress):
        self.collection.update_one({'api_run_name': api_run_name},
                                   {'$set': {'inference': progress}},
                                   upsert=True)


class DiffusionCache:
    """A cache management system for the stable diffusion models.
       The cache is a dictionary of the form:(modelid:user).
       This cache is a LRU cache, which means that the least recently used
    """
    def __init__(self, path, json_file, size=int(CACHE_SIZE)):
        self.size = size
        self.path = path
        self.json_path = os.path.join(path, json_file)
        # set the ordereddict with fixed size
        self.cache = OrderedDict()
        # if the json file exist, create it
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                self.cache = json.load(f,
                                  object_pairs_hook=OrderedDict)
        
        while len(self.cache) > self.size:
            self.cache.popitem(last=False)
    
        
    def update(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        pop_key, pop_value = None, None
        if len(self.cache) > self.size:
            pop_key, pop_value = self.cache.popitem(last=False)
        with open(self.json_path, 'w') as f:
            json.dump(self.cache, f)
        if pop_key:
            os.system(f"rm -rf {os.path.join(self.path, pop_key)}")


def files_names(bucket_name):
    """return a list of the file names in the bucket"""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]


def upload(source_dir, bucket_name, object_name):
    """zip a folder with subfolders and 
    upload to google cloud storage
    """
    archive = io.BytesIO()
    with ZipFile(archive, 'w') as zip:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zip.write(os.path.join(root, file))
    archive.seek(0)


    # upload to google cloud storage
    bucket = storage_client.bucket(bucket_name)
    blob = storage.Blob(object_name, bucket)
    blob.upload_from_file(archive,
                          content_type='application/zip')


def download(bucket_name, object_name, destination_dir):
    """download a zip file from google
    cloud storage and unzip it
    """
    # download the zip file
    bucket = storage_client.bucket(bucket_name)
    blob = storage.Blob(object_name, bucket)
    blob.download_to_filename("temp.zip")

    # unzip the file
    with ZipFile("temp.zip", 'r') as zip:
        zip.extractall(destination_dir)
    try:
        if os.path.exists("/model-cache/model-cache"):
            folder = os.listdir("/model-cache/model-cache")[0]
            os.rename(f"/model-cache/model-cache/{folder}",
                      f"/model-cache/{folder}")
            os.remove("/app/temp.zip")
            # delete the folder of model-cache/model-cache
            os.rmdir("/model-cache/model-cache")
    except:
        os.remove("/app/temp.zip")
        raise Exception("Error in downloading the model")
    