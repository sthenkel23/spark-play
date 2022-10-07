import pyspark
from pyspark.sql import SparkSession


def fake_data():
    """_summary_
    """
    spark = SparkSession.builder.getOrCreate()
    df = spark.sql("select 'spark' as hello ")
    df.show()
    return df
