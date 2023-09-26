import redis
from app.mongo_client import MongoClient, parameters
from io import BytesIO
import os
from PIL import Image
import base64

REDIS_HOST = parameters.get("REDIS_HOST")
REDIS_PORT = parameters.get("REDIS_PORT")
REDIS_PASSWORD = parameters.get("REDIS_PASSWORD")

if not REDIS_HOST or not REDIS_PORT or not REDIS_PASSWORD:
    raise Exception("Redis environment variables not set")


class RedisClient:
    """
    We use redis client to handle the storage of images. When looking up an image,
    it will first see whether it's already in the redis. 
    If it's not, it will look up for the MongoDB GridFS to get the image.
    """
    def __init__(self):
        self.db = MongoClient().db
        
        self.client = redis.Redis(host=REDIS_HOST,
                                  port=int(REDIS_PORT),
                                  password=REDIS_PASSWORD)


    def get_image(self, filename, collection="generated_images", low_res=False):
        if low_res:
            # replace the .png/.jpg/.jpeg with _low_res.png/.jpg/.jpeg
            low_res_filename = filename.replace(".png", "_low_res.png")\
                                 .replace(".jpg", "_low_res.jpg")\
                                    .replace(".jpeg", "_low_res.jpeg")
            if not self.client.exists(low_res_filename):
                image_data = self.db[collection]\
                                 .find_one({"filename": filename})['image_data']
                # downsample the image to 256x256
                image = Image.open(BytesIO(base64.b64decode(image_data.encode('utf-8'))))
                image = image.resize((256, 256))
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                self.client.set(low_res_filename, base64.b64encode(buffer.getvalue()))
            return self.client.get(low_res_filename).decode('utf-8')            
        else:
            if not self.client.exists(filename):
                image_data = self.db[collection]\
                                .find_one({"filename": filename})['image_data']
                base64_bytes = image_data.encode('utf-8')
                self.client.set(filename, base64_bytes)
            return self.client.get(filename).decode('utf-8')
