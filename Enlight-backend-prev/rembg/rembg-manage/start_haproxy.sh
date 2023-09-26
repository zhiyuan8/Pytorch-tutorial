docker run -dp 2333:9999 --name haproxy_rembg \
       -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg \
       --network enlight-net \
       --restart unless-stopped \
       enlightdev/haproxy:latest