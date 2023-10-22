from prefect import flow, serve
from sample_task import *

@flow(name="hello flow A", 
      log_prints=True)
def flow_A():
    """This is a sample hello flow A"""
    print("This is flow A")


@flow(name="hello flow B", 
      log_prints=True) 
def hello_flow():
    """This is a sample hello flow B"""
    name = getName() #Run task getName
    lastName = getLastName() #Run task getLastName
    print(f"Hello {name} {lastName}")



if __name__ == "__main__":
    hello_flow = hello_flow.to_deployment(name='test-hello-B-deployment',
                             tags=['sample tag B', 'sample tag other'],
                             interval=600) # 600 seconds
    flow_A = flow_A.to_deployment(name='test-hello-A-deployment',
                             tags=['tag A', 'tag other'])
    serve(hello_flow, flow_A)
