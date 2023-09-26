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


# Create the docker network enlight-net
if [ -z "$(docker network ls | grep enlight-net)" ]; then
    docker network create enlight-net
fi

# use nvidia to get the number of GPUs available
num_gpus=$(nvidia-smi -L | wc -l)
echo "Number of GPUs: $num_gpus"


# clear the server.conf first.
> server.conf

for i in $(seq 1 $num_gpus); do
    device_id=$((i-1))
    container_name="enlight-server-$i"
    echo "Starting container $container_name on GPU $device_id"

    server_line="server $container_name:4000 max_conns=1 weight=1;"
    echo $server_line >> server.conf
    # start the container 
    docker run -d --name $container_name \
        --network enlight-net \
        --gpus device=$device_id \
        --restart unless-stopped \
        enlightdev/rembgapi:latest
    echo "Container $container_name started."
done


# sleep 3
#----------------------------------------------------------------------------------------------------------------------#
# Till this step, we have started all the serving container.                                                           # 
# Now, we set up the load balancer using Nginx.                                                                        #
# Note that the server.conf and nginx.conf are important to define the nginx service.                                  #
#----------------------------------------------------------------------------------------------------------------------#
# docker run -d -p 2333:2333 --network enlight-net --name enlight-nginx \
#        -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
#        -v $(pwd)/server.conf:/etc/nginx/server.conf \
#        --restart unless-stopped \
#        enlightdev/enlightnginx:latest

docker run -dp 2333:4000 --network enlight-net --name haproxy \
       --restart unless-stopped \
       enlightdev/haproxy:latest