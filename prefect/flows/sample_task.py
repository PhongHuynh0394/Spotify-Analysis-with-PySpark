from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1))
def getName(name = "phong"):
    return name

@task
def getLastName(lastName = "Huynh"):
    return lastName
