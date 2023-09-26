docker stop main-api
docker rm main-api
docker image rm main-api
docker build . -t main-api --no-cache
bash start_server_local.sh
#docker attach main-api
