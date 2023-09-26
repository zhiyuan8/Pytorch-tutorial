from google.cloud import storage
import os

def remove_model(projectname, bucket_id):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_id)
    try:
        blob = bucket.blob(projectname)
        blob.delete()
    except:
        pass
    return {"message": "success"}
