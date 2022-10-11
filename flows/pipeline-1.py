from pyspark.sql import functions as F
from spark_play.utils.helper import Timer
from spark_play.transforms.synthetic_data import pd_rdn_feature_creator
from spark_play.utils.spark_session import (
    store_dataframe,
    # store_dataframe_on_gcp_bucket,
    read_dataframe,
)
from spark_play.utils.spark_session import session_builder, set_session_conf


def create_data(spark):
    """_summary_

    Args:
        spark (_type_): _description_
    """
    df = pd_rdn_feature_creator(spark, n_user=1000, n_features=5)
    df_2 = pd_rdn_feature_creator(spark, n_user=20, n_features=2)

    df_2 = df_2.selectExpr("id", "feat_0 as f_0", "feat_1 as f_1")
    with Timer("This it being timed -->>> "):
        df = df.join(F.broadcast(df_2), "id", "left")

    df = df.agg(
        F.countDistinct(F.col("id")).alias("User Count"),
        F.countDistinct(F.when(F.col("f_0").isNull(), F.col("id"))).alias("a"),
        F.countDistinct(F.when(F.col("f_0").isNotNull(), F.col("id"))).alias("b"),
        F.sum(F.when(F.col("f_0").isNull(), 1).otherwise(0)).alias("feature missing"),
        F.sum(F.when(F.col("f_0").isNotNull(), 1).otherwise(0)).alias("common features"),
    )
    print(df.show())
    store_dataframe(df, workspace="./", filename="enjoy", format="parquet")
    # store_dataframe_on_gcp_bucket(spark, df, bucket_name=os.environ["BUCKET_NAME"], filename="enjoy", format="parquet")
    pass


def read_data(spark):
    df = read_dataframe(spark, workspace="./", filename="enjoy", format="parquet")
    print(df.show())
    pass


def workflow():
    spark = session_builder()
    spark = set_session_conf(spark, **{"spark.app.name": "new_name"})

    create_data(spark)
    read_data(spark)


if __name__ == "__main__":
    workflow()
