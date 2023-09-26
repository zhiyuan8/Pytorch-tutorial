# Introduction
This repo contains the code about the dreambooth. 

It is important to set up a clean and reliable environment. We need to specify the nvidia driver and install the container toolkit to enable the docker container to use the GPU. To set up the overall environment, follow the steps below (*work for the gcloud*):
1. Install the nvidia driver
```bash
sudo apt-get install ubuntu-drivers-common \
	&& sudo ubuntu-drivers autoinstall
```
After we install the nvidia driver, we need to reboot the machine.

**Important:** If you come across any issue here, just skip this step. And continue to the next step. The docker container will automatically install the nvidia driver. 


**For development**
If you want to use the docker container for development. Refer to the [Youtube video](https://www.youtube.com/watch?v=Uvf2FVS1F8k). For example, you want to develop the dreambooth. Please just use the base docker image. After you attach the running container, it is a new linux system. You can do whatever you want there. For example, you can git clone the repo and develop the code.



2. Install the container toolkit
```bash
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install nvidia-container-runtime
```
The commands above is saved in the `env_setup.sh` file. 

# Dreambooth-Base-Docker-Image
In this repo, it contains the docker file that is used to construct the base image for the dreambooth. The `Dreambooth` folder includes the code of training and inference script.

To get the base image, we can 
```bash
./docker-build.sh
```
or (We need to install [docker compose plugin](https://docs.docker.com/compose/install/linux/) first)
```bash
docker compose up
```

Note that I set docker mount in the folder of `code`. Thus, we can develop in the folder of `code` inside the docker container.


# Dreambooth-API
In this folder, we include the api for the training and inference. The `dreambooth-api` folder includes the code of training and inference script, and the `Dockerfile`. Since we need to design a special system, we prefer the bash script here to manipulate the docker service rather than the docker compose. Thus, a bash script file called `enlightdreambooth_start.sh` is used to start the service. Note that the command insides include the usage of `Nginx`, `docker network` and `docker volume`. For the detailed process, refer to the file of `enlightdreambooth_start.sh`.

## Create the Docker image
To start the docker service, we need to first get the Docker image. Our latest version is store on our docker repo, and can be pulled to local via the following command:
```bash
$ docker pull enlightdev/enlightaidreamboothapi:latest
```

Alternatively, during development one may want to build the image from local files instead of pulling. This can be achieved by running the following command in the ``dreambooth-api`` folder:
```bash
$ docker build . -t dreambooth-api
```

## Create the Docker container

To start the docker service, we only need to use the following line inside the folder of `dreambooth-manage`:
```bash
$ bash service_start.sh
```
After that, we can access the service by `localhost:2333`.

It has the following functions:
- Make fully use of the current VM. Each GPU has a container. And it supports the concurrent training and inference.
- Local cache system. We can also pass the variable to set the some variables to control the overall service.
- The load balacing function provided by the `Nginx`.

If we need to remove the containers, use the following line:
```bash
$ bash service_stop.sh
```
This will remove all the servers and the nginx network.

**Note**: It turns out that two inferences can be hosted in one machine.


## Management of the pretrained model
All the pretrained models are saved in the google storage. Each docker container has a shared folder in the local storage to save the pretrained model. 
```bash
docker volume:some folder
```

We will need a special algorithm (*LRU*) to manage which model is necessary to be saved locally (**cache**). We will create a special docker volume to save the models and the cache file. 

**The service is ported at 5000. Thus, if you deploy it in local computer, use the link `localhost:5000`. **


## Train API
Train API is a HTTP POST request by `service/train` (service here is a http link if we deploy it). We must at least give the three parameters below:
```bash
# define the unique token like "a sks chair"
INSTANCE_PROMPT 
# define the name of the model
OUTPUT_DIR
# Set a list of base64 string of images as the input
IMAGE_LIST
```
We can also define other parameters below optionally. 

```bash
MODEL_NAME="stabilityai/stable-diffusion-2"
MAX_TRAINING_STEPS=400
RESOLUTION=768
TRAIN_BATCH_SIZE=1
LR = 2e-6
LR_SCHEDULER = "constant"
LR_WARMUP_STEPS = 0
MAIN_PROCESS_POR = 28900
GRADIENT_ACCUMULATION_STEPS=1
```
Note that we can only define parameters above, otherwise, the service will raise an error.
 
If we didn't set the parameters correctly or there is some other issues, the service will return a message of the corresponding error.

If everything runs well, the service will return a message of success. The model will be saved and be uploaded to the google storage bucket of `modelids`. After the model is saved, the local model will be removed.

An example of the POST request could be:
```json
{
    "MODEL_NAME":"stabilityai/stable-diffusion-2-1",
    "IMAGE_LIST": ["base64code1", "base64code2", "..."],
    "OUTPUT_DIR": "Alex-Model-Fun",
    "INSTANCE_PROMPT": "A sks chair",
    "MAX_TRAINING_STEPS": 400,
    "LR": 1e-6
}
```


## Inference API
For inference API, we must give the parameters of `prompt` and `model_id`. We can optionally define the `size=768` and `num_image=10` (they have default values, 768 and 10). The service is a HTTP POST accessed by `service/inference`.

If anything is wrong, the service will return a message of the corresponding error. 

If the model with `model_id` is not saved locally, the service will download the model from the google storage bucket of `modelids`. Otherwise, the serive will use the model directly. 


An example of the POST request could be:
```json
{
    "prompt":"A sks chair on the beach",
    "model_id": "Alex-Model-Fun",
    "num_image": 3
}
```

For the output, we will get a message of sucess. And we will get a list of base64 encoded images.

```json
{
  "message": "Inference is done.",
  "images": images // images are a list of base64 encoded images
}
```


# bgrem
This folder has the full name of `background removal`. It contains the `Dockerfile` to use the code.

This package make use of the [u2net](https://github.com/xuebinqin/U-2-Net) paper. There are five different models that can be used. 
- `u2net`: General model
- `u2net_cloth_seg`: Model for cloth
- `u2net_human_seg`: Model for human
- `silueta`: Lightweight version
- `u2netp`: Lightweight version

We can use the following command to start the service:
```bash
docker run -it -p 4000:4000 --name bgrem_service --gpus all enlightdev/bgrem:latest
```

As an example to use the service, refer to the following code:
```python
import requests
import json
import base64
from PIL import Image

# encode a image to base64 string
encoded_string = base64.b64encode(open("input.jpg", "rb").read()).decode('utf-8')

url = "http://127.0.0.1:4000/remove"

payload = json.dumps({
    "input_image": encoded_string
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
returned_string = response.json()['output_image']
```

After we get the base64 output, use
```python
# Decode the base64 string
# Decode the base64-encoded image
decoded_image = base64.b64decode(returned_string)
with open("output.jpg", "wb") as fh:
    fh.write(decoded_image)
```

In `rembg/k8s-config`, the yaml files used to start the service in the kubernetes cluster are saved.

Note that the route `remove` is to get the image with white background. However, if we want to get opaque background, we can use the route `remove-opacity`.


# Enlight-redis
Inside this folder, it containers the code to run the redis server. There are two aspects:
- Run a single redis server;
- Run a redis cluster.

Almost any programming language has a package to interact with the redis server. Choose the appropriate package to use then.

**Warning: The parameters that controls the function of redis is inside the config/redis.conf. Don't change it randomly or it will destroy the whole service.**

## Run a single redis server
Inside this folder, we can use the following command to run the redis server:
```bash
bash start-redis.sh
```
With a running service active at `localhost:6379`. We can use some package to connect to it like in Python or in NodeJS. 

For example, in Python, we can use 
```python
client = redis.Redis(
            host='localhost',
            port=6379,
            password='enlightai2022'
          )
```
Note that the password is set in the `enlight-redis/single_redis/config/redis.conf` file. Then, we can set and get the value of the redis server. Before we use the server, more setup about the policy is needed. In our current setup, I use
- The max memory is 4GB, and the eviction policy is `allkeys-lru`. This means if the new content comes in and the data is more than 4GB, the redis server will evict the least recently used data.;
- I set the persistence to `appendonly yes`. This means the redis server will save the data to the disk frequently. The disk and memory will sync every 1 second.
- Note that there is no default time based eviction policy, if we need it, we have to set it by hand.

Now, we talk about how to use it. The general step is to use a ecosystem between `client`, `DB` and `redis`. The steps are
```python
if data is in redis:
    redis.get(data)
else:
    data = DB.get(data)
    redis.set(data)
```
Including this step, we can accelerate the speed in `10~50` (from website blog) times. In terms of pushing data to redis, two caveats are:
- We must set expiry time if we need it. For example, in python redis, we can use `redis_client.set(key, value, ex=expiry_time)`. The `ex` means the expiry time is in seconds.
- If we need to update the value in the database. For example, the user updates his `profile_picture` in the database. There are two methods called `walk through` and `walk back`. We could delete the key in the redis server. Otherwise, the old value will be returned. In python redis, we can use `redis_client.delete(key)` to delete the key. Alternatively, we can update the value in the redis, and then the DB.

Lastly, redis is a remote dictionary server. Everything is saved as the form of key-value pair. Not like the dict in Python, the value here can be anything that can be expressed as binary. To demonstrate the usage, I use an image in redis for example:
```python
from PIL import Image
import redis
from io import BytesIO
from matplotlib import pyplot as plt

client = redis.Redis(
            host='localhost',
            port=6379,
            password='enlightai2022')

# save to redis
output = BytesIO()
im = Image.open('BasicRedis/cat.jpeg')
im.save(output, format=im.format)
client.set('imgdata', output.getvalue())
output.close()

# we can get the img as bytes
img = client.get('imgdata')
# show the img
im = Image.open(BytesIO(img))
plt.imshow(im)
```
Use bytes is even more efficient than base64 string when dealing with image.



## Run a redis cluster
The method to start up a redis server is to use the following command:
```bash
bash start_cluster.sh
``` 

To connect to the redis, we will use the following python code, which needs the installation of 
```bash
pip install redis-py-cluster
```

And the connection would be 
```python
from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "10.138.0.9", "port": "6379"},
                 {"host": "10.138.0.9", "port": "6380"}]

# Note: See note on Python 3 for decode_responses behaviour
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
rc.set("name", "enlightai")
print(rc.get("name"))
```
We can just connect to one of the node, and the redis cluster will distribute the request to appropriate node. Note that it is more a trick of network. 

The redis cluster is useful:
- It helps to do sharding. We can split the data into different nodes. For example, we can split the data into 3 nodes. Then, we can use the hash function to map the key to the node. This is useful when the data is too large to fit in one node. And it is a way to scale the service.
- The replication is also useful. We can set the replication factor to 3. Then, the data will be replicated to 3 nodes. If one node is down, the data is still available. This is useful when we need to ensure the data is available.

At this point, I use a prepared image called `bitnami/redis-cluster`. Otherwise, we can setup a redis node ready for cluster ourselves by add the following lines in the `redis.conf` file:
```bash
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
```

# dreambooth-script
We use the code inside this folder to generate the assets of dreambooth directly by Python script. It is also related to the dev by docker container. Please consider the follow steps to run the code.
1. Bring up the dreambooth base image.

```bash
docker run -it -d --name your_container_name --gpus all enlightdev/enlightaidreambooth:cu113
```

2. Attach into the container.
3. Open the folder of `root` or `home`, and copy the code inside this folder. Then, do the training and inference. 

**warning: make sure there are INPUT, Generation and OUTPUT folders created.**

This folder is used to save the latest diffusers code.


# main-api
In this folder, we can start the service by only one command:
```bash
bash start_service.sh
```
after we build the docker image. 
Or, we can direcly use `python server.py`.
To ensure the service runs correctly, make sure the environment variables provided in the `main.env` are correct. We can also change the APIs in the env file.

The service can be accessed in the port of 8040.

Note that we need to make sure the file `main.env` is in the same folder as `start_service.sh`. We can edit the `main.env` to change the environment variables so as to change the container service. Refer to the `main.env` for the details.


# mongodb-server
The server is hosted in the server called `enlight-database-vm`. To connect with the current server, we can use the following code:
```python
# connect to the MongoDB server with username and password
import pymongo

username = 'XXX'
password = 'XXX'
host = '10.138.0.7'
ports = [27117, 27118]
mongo_url = f"mongodb://{username}:{password}@{host}:{ports[0]},{host}:{ports[1]}/?authMechanism=DEFAULT"
client = pymongo.MongoClient(mongo_url)

# list all current db
dbs = client.list_database_names()
print(dbs)
```

Note that we may need to change the host if we use the internal or external port. 

The current database have the following setup:
1. Three shards, the data can be distributed into three shards. The shards are `shard1`, `shard2` and `shard3`. In this way, the read and write can be 3 times faster.
2. Three replicas, the data can be replicated into three replicas. The replicas are `replica1`, `replica2` and `replica3`. In this way, the data is more reliable. If one replica is down, the data is still available.
3. We set two routes for mongodb cluster. It is because that the mongodb cluster is not stable randomly. So, we use two routes to ensure the connection is stable. The routes are `route1` and `route2`. The route is the entry point of the cluster. We can connect to the route, and the route will connect to the cluster.

When you use the mongodb, remember to use the shard for the db and collection to accelerate the process:
```python
admin_db = client.admin
admin_db.command("enableSharding", "enlightai")
```

The current data can be up to 333 GB.


# upsampler
In this upsampler folder, we save the code for the stable diffusion upsampler service. Suppose the host is your local machine, `localhost`.

We can view the message and hostname of the service by `localhost:4455`.

To access the service, use the POST request in `localhost:4455/upsampler`. The example to access the service is as the following:
```python
import requests
import base64

url = "http://127.0.0.1:4455"

# find get message
response = requests.get(url)
print(response.json())

# input string
input_image_string = base64.b64encode(open("original.png", "rb")\
                           .read())\
                           .decode("utf-8")
url = "http://127.0.0.1:4455/upsampler"
resolution = 2048
prompt = "The sofa next to the window"
mblimit = "false"
response = requests.post(url, json={"image": input_image_string,
                                    "prompt": prompt,
                                    "resolution": resolution,
                                    "mblimit": mblimit})
status = response.json()["status"]
if status == "true":
  output_image_string = response.json()["image"]
  # save it as upsample.png
  with open("upsample.png", "wb") as f:
      f.write(base64.b64decode(output_image_string))
```

Note the following manual for the service (The best way is to see the `app.py` file inside.):
1. We must give the input of `base64 string` and `prompt`, and the prompt should be a string description of the image. For the image generated by diffusion model, we can use the original prompt.
2. The default resolution is `2048`, and there is no mblimit. 
3. The value of resolution can only be `1024` or `2048`.
3. The value of mblimit can only be `"true"` or `"false"` (string). If we select `"true"`, it output an image of `5MB`. 
5. Anytime, you get a status as "false", you can view the "message" to see what is wrong. 


# realesrgan
This uses the gan to do the upsampling. The docker image is `enlightdev/realesrganapi:latest`. The service is hosted in the port of `11111`. One can start a service by the following command:
```bash
docker run -d -p 11111:11111 --name realesrganapi --gpus all enlightdev/realesrganapi:latest
```
I recommend to use T4 GPU or better. K80 is also OK, but it may not support the large resolution and special arguments.

One can use the following python code to do the most basic upsampling (Usually enough for most of the cases):
```python
import requests
import base64

url = "http://127.0.0.1:11111"

# find get message
response = requests.get(url)
print(response.json())

# input string
input_image_string = base64.b64encode(open("original.png", "rb")\
                           .read())\
                           .decode("utf-8")
url = "http://127.0.0.1:11111/upsampler"
model_name = "RealESRGAN_x4plus"
out_resolution = 4096
response = requests.post(url, json={"input_string": input_image_string,
                                    "model_name": model_name,
                                    "out_resolution": out_resolution})
status = response.json()["status"]
print(status)
if status == "true":
  output_image_string = response.json()["image"]
  with open("upsample.png", "wb") as f:
      f.write(base64.b64decode(output_image_string))
```
Basically, we need to define the `model_name` and `out_resolution`. The `out_resolution` is the resolution of the output image. You can define the resolution as any value that is larger than 1024, such as 2048, 4000, 4096, 8K etc. 

You can also pass additional arguments like `face_enhance` and `denoise_strength`. Refer to the `app.py` for the usage.


# dev-scripts
This section will introduce how to start each service in one single machine for development. We will start `redis`, `dreambooth server`, `rembg server`, `main api` and `dashboard` in one single machine.
**Note**: MongoDB is not included since we can use the free online service.

## Start a dreamboothapi service
If you want to start a dreambooth api service seperately, modify the `main.env` file. Then, use the `start.sh` to start a runtime instance. Note that the default exposed port is `5000`. If you have multiple instantces, you can change the port to `5001`, `5002` etc.

**Note**: The reason to change `main.env` file is to change the mongodb url.

You can access the service directly in the same vm using `localhost` or use external ip after open the firewall of google vm.

## Start a rembgapi service
Use the `start.sh` to start a runtime instance. Note that the default exposed port is `4000`. There is nothing to change.

## Start a single redis server
Run `start.sh` to start the redis server. The default port is `6379`. You can change the port in the `start.sh` file.

## Start mainapi service
Be sure to edit the `main.env` file. Then, use the `start.sh` to start a runtime instance. Pay attention to the port exposed.



