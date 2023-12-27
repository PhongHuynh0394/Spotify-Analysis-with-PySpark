from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from contextlib import contextmanager
import os

@contextmanager
def MongodbIO():
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_SRV")
    cluster = cluster.split("//")[-1]
    uri = f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"
    try:
        client = MongoClient(uri)
        print(f"MongoDB Connected")
        yield client
    except ConnectionFailure:
        print(f"Failed to connect with MongoDB")
        raise ConnectionFailure
    finally:
        print("Close connection to MongoDB")
        client.close()
