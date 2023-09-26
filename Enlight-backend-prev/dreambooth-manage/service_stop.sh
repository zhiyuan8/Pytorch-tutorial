# remove all the containers starting with enlight-nginx
docker rm -f $(docker ps -a | grep enlight-nginx | awk '{print $1}')

# remove all the containers starting with enlight-proxy
docker rm -f $(docker ps -a | grep haproxy | awk '{print $1}')

# remove all the containers starting with enlight-server
docker rm -f $(docker ps -a | grep enlight-server | awk '{print $1}')