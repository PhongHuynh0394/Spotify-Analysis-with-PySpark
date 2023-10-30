from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"

@task
def connectMongo():
    # Create a new client and connect to the server
    client = MongoClient(uri)

    db = client.list_database_names()

    print('databases:')
    for db_name in db:
        print(db_name)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
