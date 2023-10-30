from prefect import flow, serve
from sample_task import *
from Ingest_Mongodb.mongodb_task import *


@flow(name="Ingest MongoDB Atlas flow", 
      log_prints=True)
def pipeline_A():
    """Test connection with MongoDB Atlas"""
    ingest_Mongodb()


@flow(name="ELT flow", 
      log_prints=True) 
def pipeline_B():
    """This is a sample hello flow B"""
    name = getName() #Run task getName
    lastName = getLastName() #Run task getLastName
    print(f"Hello {name} {lastName}")


if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                             tags=['Ingest data','MongoDB Atlas'])

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT deployment',
                             tags=['ELT'],
                             interval=600) # 600 seconds

    serve(pipeline_A, pipeline_B)
