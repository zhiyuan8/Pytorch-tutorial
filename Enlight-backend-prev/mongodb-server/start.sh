#-----------------------The process to start mongodb-server-----------------------#
# 1. Start all services.
docker-compose up -d

# sleep 30s
sleep 30

# 2. Initialte the replica sets.
docker-compose exec configsvr01 bash "/scripts/init-configserver.js"
sleep 10
docker-compose exec shard01-a bash "/scripts/init-shard01.js"
sleep 10
docker-compose exec shard02-a bash "/scripts/init-shard02.js"
sleep 10
docker-compose exec shard03-a bash "/scripts/init-shard03.js"
sleep 10

# 3. Initialte the router.
docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"
sleep 20


# 4. Setup the authentication.
docker-compose exec configsvr01 bash "/scripts/auth.js"
sleep 3
docker-compose exec shard01-a bash "/scripts/auth.js"
sleep 3
docker-compose exec shard02-a bash "/scripts/auth.js"
sleep 3
docker-compose exec shard03-a bash "/scripts/auth.js"
sleep 3


