# start the proxy service
docker run -dp 2222:9999 --network enlight-net --name haproxy-infer \
       --restart unless-stopped \
       haproxy:infer

docker run -dp 3333:9999 --network enlight-net --name haproxy-train \
       --restart unless-stopped \
       haproxy:train