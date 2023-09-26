# connect to the MongoDB server with username and password
import pymongo

username = 'enlightai'
password = 'enlightai2023CCZ'
host = '10.138.0.7'
ports = [27117, 27118]
mongo_url = f"mongodb://{username}:{password}@{host}:{ports[0]},{host}:{ports[1]}/?authMechanism=DEFAULT"
client = pymongo.MongoClient(mongo_url)

# list all current db
dbs = client.list_database_names()
print(dbs)

admin_db = client['admin']
print(admin_db.list_collection_names())