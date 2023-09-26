from flask import Flask, request, send_from_directory
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import base64
from threading import Lock
from inference_realesrgan import enlightai_upsampler

app = Flask(__name__)

@app.route('/')
def message():
    hostname = os.uname()[1]
    return {
        "message": f"Running on machine {hostname}!"
    }

# add the favicon.ico to the app
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    

@app.route('/upsampler', methods=['POST'])
def upsammpler():
    with Lock():
        data = request.json
        try:
            input_string = data['input_string']
            out_resolution = int(data['out_resolution'])
        except:
            return {
                "status": "false",
                "error": "Missing input"
                +"or output_scale"
            }
        model_name = data.get('model_name', "RealESRGAN_x4plus")
        tile_size = data.get('tile_size', 0)
        tile_pad = data.get('tile_pad', 10)
        pre_pad = data.get('pre_pad', 0)
        denoise_strength = data.get('denoise_strength', 0.5)
        face_enhance = data.get('face_enhance', False)
        fp32 = data.get('fp32', False)
        alpha_upsampler = data.get('alpha_upsampler',
                                "realesrgan")
        print("The upsampling started, please wait...")
        try:
            output_string = enlightai_upsampler(
                                model_name, input_string,
                                out_resolution,
                                tile_size, tile_pad, 
                                denoise_strength, pre_pad, 
                                face_enhance, fp32,
                                alpha_upsampler
                            )
            print("The upsampling finished.")
        except RuntimeError as error:
            return {
                "status": "false",
                "error": str(error)
            }
    return {
        "status": "true",
        "image": output_string
    }
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=11111,
            debug=False)