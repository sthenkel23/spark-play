from pyspark.sql import functions as F
from spark_play.transforms.synthetic_data import pd_rdn_feature_creator
from spark_play.utils.spark_session import store_dataframe, read_dataframe
from spark_play.utils.helper import Timer


def create_data():
    """_summary_"""
    df = pd_rdn_feature_creator(n_user=1000, n_features=5)
    df_2 = pd_rdn_feature_creator(n_user=20, n_features=2)

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
    pass


def read_data():
    from spark_play.utils.spark_session import session_builder
    spark = session_builder()
    df = read_dataframe(spark, workspace="./", filename="enjoy", format="parquet")
    print(df.show())
    pass


def workflow():
    create_data()
    read_data()


if __name__ == "__main__":
    workflow()
