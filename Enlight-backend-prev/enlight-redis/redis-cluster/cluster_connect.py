from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "10.138.0.9", "port": "6379"},
                 {"host": "10.138.0.9", "port": "6380"}]

# Note: See note on Python 3 for decode_responses behaviour
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
# rc.set("name", "enlightai")
print(rc.get("name"))