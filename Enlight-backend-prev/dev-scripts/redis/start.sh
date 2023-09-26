# Description: Start a single redis instance

# check if there is docker volume for redis
if [ -z "$(docker volume ls | grep enlight-redis)" ]; then
    docker volume create enlight-redis
fi


# redis-server /etc/redis/redis.conf is the CMD command
docker run -it --rm -dp 6379:6379 --name enlight-redis \
    -v ${PWD}/config:/etc/redis/ \
    -v enlight-redis:/data/ \
    redis:6.0-alpine redis-server /etc/redis/redis.conf