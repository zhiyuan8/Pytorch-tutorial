from dotenv import load_dotenv, dotenv_values
from flask import Flask, jsonify, request
import os
from pathlib import Path
import subprocess
from inference import inference_func
from Utils import (files_names, upload, 
                   download, LogInfo, DiffusionCache)
import base64
import torch
import gc
from threading import Lock

requests_lock = Lock()

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
dotenv_path = Path('enlight.env')
parameters = dotenv_values(dotenv_path=dotenv_path)

diffusion_cache = DiffusionCache(
                            "/model-cache",
                            "cache.json"
                        )


# Indicate our application is successful.
@app.route('/', methods = ['GET'])
def test():
    with requests_lock:
        hostname = os.uname()[1]
    return jsonify({"message": f"It works and runs on {hostname}"})


# conduct the training
@app.post('/train')
def train():
    with requests_lock:
        # clear all the memory 
        torch.cuda.empty_cache()
        gc.collect()
        # Get the training parameters from the request
        load_dotenv(dotenv_path=dotenv_path)
        data = request.json
        try:
            prompt = data['INSTANCE_PROMPT']
            model_id = data['OUTPUT_DIR']
            # set the input of the training script
            image_list = data['IMAGE_LIST']
        except:
            return jsonify({"error": "You must at least provide"+
                            " INSTANCE_PROMPT, MODEL_ID and OUTPUT_DIR."})
        
        saved_model_path = f"/model-cache/{model_id}"
        data['OUTPUT_DIR'] = saved_model_path
        for key in data.keys():
            if key in parameters.keys():
                os.environ[key] = str(data[key])
            elif key != "IMAGE_LIST":
                return jsonify({"error": "Invalid parameter provided."})
        
        # set a temporary folder to store the images
        temp_image_folder = f"{model_id}_temp_images"
        # create the temporary folder
        os.system(f"mkdir {temp_image_folder}")
        for encoded_string in image_list:
            binary_data = base64.b64decode(encoded_string)
            with open(f"{temp_image_folder}/{image_list.index(encoded_string)}.png",
                    'wb') as f:
                f.write(binary_data)
        os.environ['INSTANCE_DIR'] = temp_image_folder
        try:
            subprocess.call(['bash', 'training.sh'])
        except:
            os.system(f"rm -rf {temp_image_folder}")
            os.system(f"rm -rf {saved_model_path}")
            return jsonify({"error": "Training failed."})
        upload(saved_model_path, "modelids", model_id)
        
        # delete the temporary folder
        os.system(f"rm -rf {temp_image_folder}")
        diffusion_cache.update(model_id, model_id)
        torch.cuda.empty_cache()
    return jsonify({"message": "Training is done. The model,"+
                    f" {model_id}, is uploaded to the cloud."})


# do reference
@app.post('/inference')
def inference():
    with requests_lock:
        torch.cuda.empty_cache()
        data = request.json
        kargs = {}
        try:
            prompt = data['prompt']
            model_id = data['model_id']
            # every time we do inference, we will a api run
            # name to record the result in the cloud
            api_run_name = data['api_run_name']
            kargs['prompt'] = prompt
            kargs['model_id'] = model_id
            kargs['api_run_name'] = api_run_name
        except:
            return jsonify({"error": "You must al least provide" + 
                            "a prompt, model_id and api_run_name."})

        if model_id not in files_names("modelids"):
            return jsonify({"error": "The model_id is not found"+
                                    "in our database."})
        
        # if model_id not in model cache, download it
        if model_id not in os.listdir('/model-cache'):
            print("Downloading model...")
            # download to the model-cache folder
            download("modelids", model_id, "/model-cache")
            print("Downloading is done.")

        for key in data.keys():
            if key in {"num_image", "size", "prompt",
                    "model_id", "api_run_name"}:
                kargs[key] = data[key]
            else:
                return jsonify({"error": "Invalid parameter provided."})
        
        prompt = kargs['prompt']
        size = kargs.get('size', 768)
        num_image = kargs.get('num_image', 10)
        saved_model_path = f"/model-cache/{model_id}"
        try:
            images = inference_func(saved_model_path, prompt, 
                                    size, num_image, api_run_name)
        except:
            return jsonify({"error": "Inference failed."})
        diffusion_cache.update(model_id, model_id)
        torch.cuda.empty_cache()
    return jsonify({"message": "Inference is done.",
                    "images": images})


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)),
            host='0.0.0.0',
            debug=False, processes=1)
    