from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler
import torch
import os
import base64
import gc
from PIL import Image
import io
from Utils import LogInfo
import warnings
warnings.filterwarnings("ignore")
loginfo = LogInfo()


def inference_func(model_id, prompt, size, num_image, api_run_name):
    pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                revision="fp16").to("cuda")
    images = []
    for i in range(num_image):
        image = pipe(prompt, height=size, width=size).images[0]
        im_bytes = io.BytesIO()
        image.save(im_bytes, format='PNG')
        im_bytes = im_bytes.getvalue()
        im_base64 = base64.b64encode(im_bytes).decode()
        images.append(im_base64)
        loginfo.update_inference_progress(api_run_name, float((i+1)/num_image))
    del pipe
    gc.collect()
    torch.cuda.empty_cache()
    return images

