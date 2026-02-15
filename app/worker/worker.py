import redis
from pymongo import MongoClient
import os
import time

redis_host = os.getenv("REDIS_HOST", "redis")
mongo_uri = os.getenv("MONGO_URI")

r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
mongo = MongoClient(mongo_uri)
db = mongo.voting
votes = db.votes

print("Worker started...")

while True:
    vote = r.brpop("votes", timeout=5)
    if vote:
        votes.insert_one({"vote": vote[1]})
        print("Saved vote:", vote[1])
    time.sleep(1)
