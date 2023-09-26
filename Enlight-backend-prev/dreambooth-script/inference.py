from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler
import torch
import os
import base64
from PIL import Image
import io
import warnings
warnings.filterwarnings("ignore")

#-----------------------Set the input parameters-----------------------#
model_id = 'OUTPUT'
prompt="A photo of a sks person wearing the marvel universe ironman suit, digital art style"
size = 768
num_image = 10
#----------------------------------------------------------------------#


pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                revision="fp16").to("cuda")
for i in range(num_image):
    image = pipe(prompt, height=size, width=size).images[0]
    image.save(os.path.join('Generation', str(i+1)+'.png'))

del pipe, image    
torch.cuda.empty_cache()

