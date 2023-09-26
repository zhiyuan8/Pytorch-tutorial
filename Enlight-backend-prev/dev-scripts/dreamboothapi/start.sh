# check if we install nvidia-container-runtime
if [ -z "$(dpkg -l | grep nvidia-container-runtime)" ]; then
    echo "Current VM does not have nvidia-container-runtime installed."
    echo "Now installing..."
    curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
    sudo apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
    sudo apt-get update
    sudo apt-get install nvidia-container-runtime
    echo "nvidia-container-runtime installed."
    # sleep 10 seconds
    sleep 5
fi


# Create a docker volume to save the local models
# called model-cache
if [ -z "$(docker volume ls | grep model-cache)" ]; then
    docker volume create model-cache
fi


# Create the docker network enlight-net
if [ -z "$(docker network ls | grep enlight-net)" ]; then
    docker network create enlight-net
fi

docker run --init -d --name $container_name \
        --network enlight-net \
        --gpus device=$device_id \
        --restart unless-stopped \
        -v model-cache:/model-cache \
        -v $(pwd)/main.env:/app/main.env \
        -p 5000:5000 \
        -e CACHE_SIZE=200 \
        enlightdev/enlightaidreamboothapi:cu113