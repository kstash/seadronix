from pymongo import MongoClient
import gridfs
import os


mongodb_host: str = os.getenv("MONGODB_HOST", "localhost")
mongodb_port: int = int(os.getenv("MONGODB_PORT", 27017))


client = MongoClient(host=mongodb_host, port=mongodb_port)

db = client["videos"]

if "info" not in db.list_collection_names():
    info_collection = db.create_collection("info")
else:
    info_collection = db["info"]

slice_video_collection = gridfs.GridFS(db, collection="slice_video")

# bucket = gridfs.GridFSBucket(db)