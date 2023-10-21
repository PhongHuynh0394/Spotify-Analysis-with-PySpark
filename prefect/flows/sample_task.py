from prefect import task

@task
def getName(name = "phong"):
    return name

@task
def getLastName(lastName = "Huynh"):
    return lastName
