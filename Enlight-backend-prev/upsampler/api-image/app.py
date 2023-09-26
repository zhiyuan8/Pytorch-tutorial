from flask import Flask, jsonify, request
import os
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionUpscalePipeline
import torch
import base64
import math

app = Flask(__name__)

# Utils function to process the image
class DiffusionUpsampler:
    def __init__(self, model_id="stabilityai/stable-diffusion-x4-upscaler"):
        self.pipeline = StableDiffusionUpscalePipeline.from_pretrained(  
                                               model_id,
                                               torch_dtype=torch.float16
                                            )
        self.pipeline = self.pipeline.to("cuda")
        self.pipeline.set_use_memory_efficient_attention_xformers(True)
    
    def resize(self, image, ratio):
        image = image.resize((int(image.size[0] * ratio),
                              int(image.size[1] * ratio)))
        return image
        
    def upsample(self, prompt, image):
        upscaled_image = self.pipeline(
                            prompt=prompt,
                            image=image)\
                         .images[0]
        return upscaled_image


@app.route('/')
def message():
    hostname = os.uname()[1]
    return {
        "message": f"Running on machine {hostname}!"
    }


@app.post('/upsampler')
def upsample():
    data = request.json
    try:
        base64string = data["image"]
        prompt = data["prompt"]
    except:
        return {
            "status": "false",
            "message": "Input the image and prompt"
        }
    resolution = int(data.get("resolution", 4096))
    mblimit = str(data.get("mblimit", "false"))
    diffusion_upsampler = DiffusionUpsampler()
    image = Image.open(BytesIO(base64.b64decode(base64string)))
    if not image:
        print("image is none!!!")
    # find min size of image, and which is smaller
    image_size = max(image.size[0], image.size[1])
    if image_size < 512:
        return {
            "status": "false",
            "message": "Input the image size larger than 512"
        }
    else:
        if resolution == 1024: ratio = 256 / image_size
        elif resolution == 2048: ratio = 512 / image_size
        else: ratio = 1
        image = diffusion_upsampler.resize(image, ratio)
        try:
            upsampled_image = diffusion_upsampler.upsample(
                                prompt, image
                            )
        except:
            return {
                "status": "false",
                "message": "Current image can't be upsampled"
            }
        if mblimit == "true":
            # limit is 5MB
            if upsampled_image.size > 5e6:
                # resize it to 4.9MB
                ratio = math.sqrt(5e6 / upsampled_image.size)
                upsampled_image = diffusion_upsampler.resize(
                                    upsampled_image, ratio
                                )
    im_bytes = BytesIO()
    upsampled_image.save(im_bytes, format="PNG")
    im_bytes = im_bytes.getvalue()
    upsampled_string = base64.b64encode(im_bytes).decode("utf-8")
    return {
        "status": "true",
        "message": "success",
        "image": upsampled_string
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=4455,
            debug=False)
            
        
    
    