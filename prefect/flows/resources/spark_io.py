from pyspark.sql import SparkSession
from pyspark import SparkConf
from contextlib import contextmanager

@contextmanager
def SparkIO(conf: SparkConf = SparkConf()):
    print('enter Spark')
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    try:
        yield spark
    finally:
        print('Stop spark')
        spark.stop()

