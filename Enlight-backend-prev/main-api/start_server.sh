# Start the service locally
# docker run -it -dp 8040:8040 --name main-api \
#     -v $(pwd)/main.env:/dashapp/main.env \
#     --network enlight-main-net \
#     enlightdev/mainapi:latest


# Use docker service and set replicas to 3
docker service create --name mainapi \
    -dp 8040:8040 \
    --replicas 4 \
    enlightdev/mainapi:latest



# Use the tool below to monitor our service.
docker service create \
  --name portainer \
  --publish 19000:9000 \
  --replicas=1 \
  --constraint 'node.role == manager' \
  --mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
  portainer/portainer-ce \
  -H unix:///var/run/docker.sock
