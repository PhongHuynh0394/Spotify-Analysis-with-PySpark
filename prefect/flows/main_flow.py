from flows.mongodb_task import connectMongo
from prefect import flow, serve
from sample_task import *
from mongodb_task import *
from dotenv import load_dotenv

# Load env
load_dotenv()
user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"

@flow(name="Ingest MongoDB Atlas", 
      log_prints=True)
def pipeline_A():
    """Test connection with MongoDB Atlas"""
    connectMongo()


@flow(name="hello flow B", 
      log_prints=True) 
def pipeline_B():
    """This is a sample hello flow B"""
    name = getName() #Run task getName
    lastName = getLastName() #Run task getLastName
    print(f"Hello {name} {lastName}")



if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB',
                             tags=['Ingest data','MongoDB Atlas'])

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT',
                             tags=['ELT'],
                             interval=600) # 600 seconds
    serve(pipeline_A, pipeline_B)
