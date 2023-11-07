from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from contextlib import contextmanager
import os

@contextmanager
def MongodbIO(database_name: str = "testDB"):
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"
    try:
        client = MongoClient(uri)
        print(f"MongoDB Connected with database {database_name}")
        yield client[database_name]
    except Exception as e:
        print(f"Failed to connect with {database_name} database")
        print(e)
    finally:
        print("Close connection to MongoDB")
        client.close()
