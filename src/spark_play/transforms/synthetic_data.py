import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
import pyspark.sql.types as T
from spark_play.data.ssql_queries import HELLO_WORLD
from spark_play.utils.spark_session import (
    define_dataset_with_query,
    define_dataset_with_pandas_dataframe,
)
from spark_play.utils.features import sequence_explode, create_features


def pd_dataset_creator(
    spark: SparkSession, query: str = HELLO_WORLD, type: str = "pandas"
) -> pd.DataFrame:
    """_summary_

    Args:
        query (_type_, optional): _description_. Defaults to HELLO_WORLD.

    Returns:
        pd.DataFrame: _description_
    """
    df = define_dataset_with_query(spark, query)
    return (df).toPandas()


def pd_rdn_feature_creator(spark: SparkSession, n_user: int, n_features: int) -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.DataFrame()
    df["id"] = np.arange(0, n_user, 1)
    df["gid"] = df["id"].astype(str)
    df = define_dataset_with_pandas_dataframe(spark, df)
    df = sequence_explode(df)

    w = Window.partitionBy("gid").orderBy(["weekofyear"])
    df = df.withColumn("idx", F.row_number().over(w))
    df = create_features(df, n_features)
    return df


def create_spark_dataframe(spark: SparkSession):
    schema = T.StructType(
        [
            T.StructField("id", T.StringType(), True),
            T.StructField("name", T.IntegerType(), True),
            T.StructField("attr_one", T.DoubleType(), True),
            T.StructField("attr_two", T.DoubleType(), True),
        ]
    )
    data = []
    return spark.createDataFrame(data, schema)
