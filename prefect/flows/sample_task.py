from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(name="get name task",
      description="This is task to generate a Name",
      cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1),
      task_run_name="Get {name}",
      tags=["Name tag"])
def getName(name = "phong"):
    """This task retrun the name"""
    return name

@task(name="Get last Name task",
      retries=3,
      tags=['Lastname tag'])
def getLastName(lastName = "Huynh"):
    """This task return the lastName"""
    return lastName
