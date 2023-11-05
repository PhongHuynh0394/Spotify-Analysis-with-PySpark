from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(name="get name task",
      description="Extract data from MongoDB to HDFS at bronze layer",
      cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1),
      task_run_name="bronze_{table_name}",
      tags=["bronze layer", "pyspark"])
def bronze_table(spark, table_name: str) -> None:
    """Extract data from MongoDB to HDFS at bronze layer"""
    return name

@task(name="Get last Name task",
      retries=3,
      tags=['Lastname tag'])
def getLastName(lastName = "Huynh"):
    """This task return the lastName"""
    return lastName

@flow
def IngestHadoop()
