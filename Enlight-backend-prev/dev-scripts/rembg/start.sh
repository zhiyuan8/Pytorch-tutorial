docker run -d --name $container_name \
        --network enlight-net \
        --gpus device=$device_id \
        -p 4000:4000 \
        --restart unless-stopped \
        enlightdev/rembg-api:latest