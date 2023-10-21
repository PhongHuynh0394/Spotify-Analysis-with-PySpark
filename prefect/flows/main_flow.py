from prefect import task, flow
from sample_task import *

@flow(name="hello_flow", log_prints=True) 
def hello_flow():
    name = getName()
    lastName = getLastName()
    print(f"Hello {name} {lastName}")

if __name__ == "__main__":
    hello_flow.serve(name='test-deployment')
