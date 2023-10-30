from pymongo.mongo_client import MongoClient

password = 123
uri = f"mongodb+srv://root:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"

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
