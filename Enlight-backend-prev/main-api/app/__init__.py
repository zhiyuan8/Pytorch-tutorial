from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app import image_storage_api
from app import dreambooth_api
from app import project_info_api
from app import bookmark_api
from app import user_info_api
from app import landingpage_api