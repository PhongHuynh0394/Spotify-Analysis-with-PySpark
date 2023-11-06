from pymongo import MongoClient
from contextlib import contextmanager
import os

@contextmanager
def MongodbIO(database_name: str = "testDB"):
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    try:
        yield client[database_name]
    finally:
        client.close()
