from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.streaming import StreamingContext
import pandas as pd


def session_builder(name: str = "my_app") -> SparkSession:
    """_summary_

    Args:
        name (str, optional): _description_. Defaults to "my_app".

    Returns:
        SparkSession: _description_
    """
    return SparkSession.builder.master("local").appName(name).getOrCreate()


def set_session_conf(spark: SparkSession, **kwargs) -> SparkSession:
    """_summary_

    Args:
        spark (SparkSession): _description_

    Returns:
        SparkSession: _description_
    """
    for c in spark.sparkContext.getConf().getAll():
        print(c)
    for k, v in kwargs.items():
        print("\n\nSet spark config to \n")
        print(k, v)
        spark.conf.set(k, v)
    return spark


def start_stream(spark: SparkSession, time: int):
    """_summary_

    Args:
        spark (SparkSession): _description_
        time (int): _description_

    Returns:
        _type_: _description_
    """
    ssc = StreamingContext(spark, time)
    ssc.checkpoint("checkpoint_RDD_recover")
    return ssc


def define_dataset_with_query(spark: SparkSession, query: str) -> DataFrame:
    """_summary_

    Args:
        spark (SparkSession): _description_
        query (str): _description_

    Returns:
        DataFrame: _description_
    """
    return spark.sql(query)


def define_dataset_with_pandas_dataframe(spark: SparkSession, df: pd.DataFrame) -> DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        spark (SparkSession): _description_

    Returns:
        DataFrame: _description_
    """
    return spark.createDataFrame(df)


def store_dataframe(
    df: DataFrame, workspace: str, filename: str, format: str, mode: str = "overwrite"
):
    """_summary_

    Args:
        df (DataFrame): _description_
        workspace (str): _description_
        filename (str): _description_

    Returns:
        _type_: _description_
    """
    return (
        df.coalesce(1)
        .write.option("header", "true")
        .mode(mode)
        .parquet(f"{workspace}/data/{filename}.{format}")
    )


def store_dataframe_on_gcp_bucket(
    spark: SparkSession,
    df: DataFrame,
    bucket_name: str,
    filename: str,
    format: str,
    mode: str = "overwrite",
):
    """_summary_

    Args:
        df (DataFrame): _description_
        workspace (str): _description_
        filename (str): _description_

    Returns:
        _type_: _description_
    """
    # spark.conf.set("spark.jars", f'{}/gcs-connector-hadoop2-latest.jar')

    return (
        df.coalesce(1)
        .write.option("header", "true")
        .mode(mode)
        .parquet(f"gs://{bucket_name}/data/{filename}.{format}")
    )


def read_dataframe(spark: SparkSession, workspace: str, filename: str, format: str) -> DataFrame:
    """_summary_

    Args:
        spark (SparkSession): _description_
        workspace (str): _description_
        filename (str): _description_
        format (str): _description_
    """
    return spark.read.parquet(f"{workspace}/data/{filename}.{format}")


def read_dataframe_from_gcp_bucket(
    spark: SparkSession, bucket_name: str, filename: str, format: str
) -> DataFrame:
    """_summary_

    Args:
        spark (SparkSession): _description_
        bucket_name (str): _description_
        filename (str): _description_
        format (str): _description_

    Returns:
        DataFrame: _description_
    """
    return spark.read.parquet(f"gs://{bucket_name}/data/{filename}.{format}")
