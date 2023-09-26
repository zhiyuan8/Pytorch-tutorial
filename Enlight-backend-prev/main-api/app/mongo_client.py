import pymongo
import os

# read the environment variables
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

dotenv_path = Path('main.env')
parameters = dotenv_values(dotenv_path=dotenv_path)

MONGO_DB = parameters.get('MONGO_DB')
MONGO_URL = parameters.get('MONGO_URL')
MONGO_PAGE_DB = parameters.get('MONGO_PAGE_DB')

if not MONGO_DB or not MONGO_URL:
    raise Exception("MONGO_DB and MONGO_URL must be set as environment variables.")

class MongoClient:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URL,
                                          serverSelectionTimeoutMS=5000)
        self.db = self.client[MONGO_DB]
        self.initiate_indexes()


    def initiate_indexes(self):
        db = self.db
        collection = db["projects"]
        if 'projectsearch' not in collection.index_information().keys():
            collection.create_index([('username', pymongo.HASHED)],
                                    name='projectsearch')
        if "projectsearch2" not in collection.index_information().keys():
            collection.create_index([('project_id', pymongo.ASCENDING)],
                                    name='projectsearch2')
            
        collection = db["users"]
        if 'usersearch' not in collection.index_information().keys():
            collection.create_index([('username',
                                      pymongo.HASHED)],
                                    name='usersearch')
        
        collection = db['progress']
        if 'apirunsearch' not in collection.index_information().keys():
            collection.create_index([('api_run_name',
                                      pymongo.HASHED)],
                                    name='apirunsearch')
        
        
        collection = db['source_images']
        if 'sourceimagesearch' not in collection.index_information().keys():
            collection.create_index([('username', pymongo.HASHED),
                                     ('project_id', pymongo.ASCENDING)],
                                    name='sourceimagesearch')
        if not 'sourceimagesearch2' in collection.index_information().keys():
            collection.create_index([('uploadDate', pymongo.DESCENDING)],
                                    name='sourceimagesearch2')
        if not 'sourceimagesearch3' in collection.index_information().keys():
            collection.create_index([('filename', pymongo.HASHED)],
                                    name='sourceimagesearch3')
        
        
        collection = db['generated_images']
        if 'generatedimagesearch' not in collection.index_information().keys():
            collection.create_index([('username', pymongo.HASHED),
                                     ('project_id', pymongo.ASCENDING),
                                     ('prompt_id', pymongo.ASCENDING)],
                                    name='generatedimagesearch')
        if not 'generatedimagesearch2' in collection.index_information().keys():
            collection.create_index('uploadDate',
                                    expireAfterSeconds = 86400,
                                    partialFilterExpression = {'bookmarked': False},
                                    name='generatedimagesearch2')
        if not 'generatedimagesearch3' in collection.index_information().keys():
            collection.create_index([('filename', pymongo.HASHED)],
                                    name='generatedimagesearch3')
        if not 'generatedimagesearch4' in collection.index_information().keys():
            collection.create_index([('bookmarked', pymongo.ASCENDING)],
                                    name='generatedimagesearch4')
            
            
        collection = db['prompts']
        if "promptsearch" not in collection.index_information().keys():
            collection.create_index([('username', pymongo.HASHED)],
                                    name='promptsearch')
        if not 'promptsearch2' in collection.index_information().keys():
            collection.create_index([('project_id', pymongo.DESCENDING)],
                                    name='promptsearch2')
        if not 'promptsearch3' in collection.index_information().keys():
            collection.create_index([('prompt_id', pymongo.DESCENDING)],
                                    name='promptsearch3')
            
        # Now initiate the index in client['contact_message']['contact_info']
        collection = self.client[MONGO_PAGE_DB]["contact_info"]
        if not "contactsearch1" in collection.index_information().keys():
            collection.create_index([('email', pymongo.HASHED)],
                                    name='contactsearch1')
        if not "contactsearch2" in collection.index_information().keys():
            collection.create_index([('datetime', pymongo.DESCENDING)],
                                    name='contactsearch2')
                
        
        
        
        