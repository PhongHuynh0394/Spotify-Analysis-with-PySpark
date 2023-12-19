from pyspark.sql import SparkSession
from pyspark import SparkConf
from contextlib import contextmanager

@contextmanager
def SparkIO(conf: SparkConf = SparkConf()):
    app_name = conf.get("spark.app.name")
    master = conf.get("spark.master")
    print(f'Create SparkSession app {app_name} with {master} mode')
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    try:
        yield spark
    except Exception:
        raise Exception
    finally:
        print(f'Stop SparkSession app {app_name}')
        spark.stop()

