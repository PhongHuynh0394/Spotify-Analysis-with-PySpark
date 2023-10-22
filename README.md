# PySpark Practice

`There is some new notebook can be use to practice with spark sql and spark dataframe. Cheer :)))`

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
