import pyspark
from pyspark.sql import SparkSession

from spark_play.data.query import HELLO_WORLD


def fake_data():
    """_summary_
    """
    spark = SparkSession.builder.getOrCreate()
    df = spark.sql(
        HELLO_WORLD
    )
    df.show()
    return df
