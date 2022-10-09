import pandas as pd
import numpy as np
from pyspark.sql.window import Window
import pyspark.sql.functions as F
import pyspark.sql.types as T
from spark_play.data.ssql_queries import HELLO_WORLD
from spark_play.utils.spark_session import (
    session_builder,
    set_session_conf,
    define_dataset_with_query,
    define_dataset_with_pandas_dataframe,
)
from spark_play.utils.features import sequence_explode, create_features


def pd_dataset_creator(query: str = HELLO_WORLD, type: str = "pandas") -> pd.DataFrame:
    """_summary_

    Args:
        query (_type_, optional): _description_. Defaults to HELLO_WORLD.

    Returns:
        pd.DataFrame: _description_
    """
    spark = session_builder()
    spark = set_session_conf(spark, **{"spark.app.name": "new_name"})
    df = define_dataset_with_query(spark, query)
    return (df).toPandas()


def pd_rdn_feature_creator(n_user: int, n_features: int) -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.DataFrame()
    df["id"] = np.arange(0, n_user, 1)
    df["gid"] = df["id"].astype(str)
    spark = session_builder()
    spark = set_session_conf(spark, **{"spark.app.name": "new_name"})
    df = define_dataset_with_pandas_dataframe(spark, df)
    df = sequence_explode(df)

    w = Window.partitionBy("gid").orderBy(["year", "biweek"])
    df = df.withColumn("idx", F.row_number().over(w))
    df = create_features(df, n_features)
    return df


def create_spark_dataframe():
    spark = session_builder()
    spark = set_session_conf(spark, **{"spark.app.name": "new_name"})
    schema = T.StructType([
        T.StructField("id", T.StringType(), True),
        T.StructField("name", T.IntegerType(), True),
        T.StructField("attr_one", T.DoubleType(), True),
        T.StructField("attr_two", T.DoubleType(), True),
    ])
    data = []
    return spark.createDataFrame(data, schema)
