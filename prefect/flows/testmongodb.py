from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")

password = 123
# public="jiowdstr"
# private="0b24c5ce-b981-4885-a202-73457caf5925"
uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"
# connection_string = f"mongodb+srv://{private}@clustername.mongodb.net/test?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# client = MongoClient(connection_string)

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
