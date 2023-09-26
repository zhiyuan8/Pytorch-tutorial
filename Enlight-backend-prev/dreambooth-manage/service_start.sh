#----------------------------------------------------------------------------------------------------------------------#
#    Preparation job.                                                                                                  #
#    Ensure there is nvidia container toolkit                                                                          #
#    Prepare the docker volume and network.                                                                            #
#----------------------------------------------------------------------------------------------------------------------#
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


# use nvidia to get the number of GPUs available
num_gpus=$(nvidia-smi -L | wc -l)
echo "Number of GPUs: $num_gpus"


# clear the server.conf first.
# > train/server.conf
# > infer/server.conf

# for i in $(seq 1 $num_gpus); do
#     device_id=$((i-1))
#     container_name="enlight-server-$i"
#     echo "Starting container $container_name on GPU $device_id"

    # server_line="server $container_name:5000 max_conns=1 weight=1;"
    # if i is odd, send serverline to train_server.conf
    # else to the infer_server.conf
    # if [ $((i%2)) -eq 1 ]; then
    #     echo $server_line >> train/server.conf
    # else
    #     echo $server_line >> infer/infer_server.conf
    # fi
    docker run --init -d --name enlight-server-3 \
        --network enlight-net \
        --gpus device=1 \
        --restart unless-stopped \
        --runtime=nvidia \
        -v model-cache:/model-cache \
        -v $(pwd)/main.env:/app/main.env \
        -e CACHE_SIZE=200 \
        enlightdev/enlightaidreamboothapi:117nvidiaruntime
#     echo "Container $container_name started."
# done

# sleep 3
#----------------------------------------------------------------------------------------------------------------------#
# Till this step, we have started all the serving container.                                                           # 
# Now, we set up the load balancer using Nginx.                                                                        #
# Note that the server.conf and nginx.conf are important to define the nginx service.                                  #
#----------------------------------------------------------------------------------------------------------------------#

# docker run -d -p 3333:2333 --network enlight-net --name enlight-nginx-train \
#        -v $(pwd)/train/nginx.conf:/etc/nginx/conf.d/default.conf \
#        -v $(pwd)/train/server.conf:/etc/nginx/server.conf \
#        --restart unless-stopped \
#        enlightdev/enlightnginx:latest


# docker run -d -p 2222:2333 --network enlight-net --name enlight-nginx-infer \
#        -v $(pwd)/infer/nginx.conf:/etc/nginx/conf.d/default.conf \
#        -v $(pwd)/infer/server.conf:/etc/nginx/server.conf \
#        --restart unless-stopped \
#        enlightdev/enlightnginx:latest