docker service create --name dashboard \
        --replicas 3 \
        -dp 23000:3000 \
        enlightdev/dashboard:latest