# if not docker network called redis-cluster, create it
if [ -z "$(docker network ls | grep redis-cluster)" ]; then
    docker network create redis-cluster
fi

# if not redis-cluster-data-1~6 volumes, create them
for i in {1..6}; do
    if [ -z "$(docker volume ls | grep redis-cluster-data-$i)" ]; then
        docker volume create redis-cluster-data-$i
    fi
done


docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
           --name redis1 --network redis-cluster -p 6379:6379 \
           -v redis-cluster-data-1:/bitnami/redis/data \
           -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
           -d bitnami/redis-cluster:latest

docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
            --name redis2 --network redis-cluster -p 6380:6379 \
            -v redis-cluster-data-2:/bitnami/redis/data \
            -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
            -d bitnami/redis-cluster:latest

docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
            --name redis3 --network redis-cluster -p 6381:6379 \
            -v redis-cluster-data-3:/bitnami/redis/data \
            -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
            -d bitnami/redis-cluster:latest

docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
            --name redis4 --network redis-cluster -p 6382:6379 \
            -v redis-cluster-data-4:/bitnami/redis/data \
            -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
            -d bitnami/redis-cluster:latest

docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
            --name redis5 --network redis-cluster -p 6383:6379 \
            -v redis-cluster-data-5:/bitnami/redis/data \
            -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
            -d bitnami/redis-cluster:latest

docker run -e ALLOW_EMPTY_PASSWORD=yes -e REDIS_NODES=redis1,redis2,redis3,redis4,redis5,redis6 \
            --name redis6 --network redis-cluster -p 6384:6379 \
            -v redis-cluster-data-6:/bitnami/redis/data \
            -v ${PWD}/config:/opt/bitnami/redis/mounted-etc/overrides.conf \
            -d bitnami/redis-cluster:latest
echo "create redis cluster..."
sleep 10

# try to run the following command, if failed, skip it
docker exec -it redis1 redis-cli --cluster create redis1:6379 redis2:6379 redis3:6379 redis4:6379 redis5:6379 redis6:6379 --cluster-replicas 1 --cluster-yes
echo "It is OK if there is error message above, since we may start from an existing cluster."
echo "redis cluster created"
