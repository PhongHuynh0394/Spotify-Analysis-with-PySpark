# Prefect Branch !!

New features added:
- Makefile (alias command)
- prefect-compose.yml (docker compose for prefect)
- Added connecting mongodb flow

## To Test Prefect
Run the following command:
```bash
make prefect-build
```
This will build a prefect images with requirements.txt in prefect folder

Wait for a second for everything build up, then start services: `make prefect-up`

Reversely, run `make prefect-down` to turn off services

Check `port 4200` to visit Prefect UI. You will see there is a flow already in `flows run` or `Deployments` section. 

**To Run pipeline:** Just trigger the `Run` button on prefect UI, there is 1 sample basic flow and 1 schedule flow for auto run

**Pipeline Structure Files:**
- Sample flow: [main_flow.py](./prefect/flows/main_flow.py) (This file has 2 flows)
- Sample tasks: [sample_task.py](./prefect/flows/sample_task.py) (this file also has 2 tasks)
- Mongodb connection task: [mongodb_task.py](./prefect/flows/Ingest_Mongodb/mongodb_task.py)

Checkout the data from Mongodb Atlas Cloud

# PySpark

## Prerequisite

Create .Env file using the following command
```bash
cp env_template .env
```

Then run in your terminal to start up all docker services
```bash
docker compose up -d
```
**Note**: Spark Cluster is optional choice, we are able to use only PySpark with `localmode` to test code with HDFS

To exec into container, open Docker Desktop or using the following command:
```bash
docker exec -it <container-id-or-name> bash
```

## Port
Check ports on your browers:
- [`localhost:9870`](http://localhost:9870): Namenode
- [`localhost:9864`](http://localhost:9864): Datanode
- [`localhost:8888`](http://localhost:8888/lab?token=pass): notebook (token=pass if you only access to port 8888)
- [`localhost:8080`](http://localhost:8080): Spark master (if uncomment Spark master service)
- [`localhost:8081`](http://localhost:8081): Spark worker(if uncomment Spark worker service)

## Usage
There is a sample Test_Pyspark jupyter file in workspace to test connection of pyspark with hdfs in `local mode` and `cluster mode`

## References

[Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)
