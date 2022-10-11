from pyspark.sql import DataFrame
from pyspark.sql.functions import rand
from functools import reduce
from pyspark.sql import functions as F, types as T


cfg2col = {"week": "weekofyear"}
PK = ["gid", "year", cfg2col["week".split()[1]] if "week" not in cfg2col else cfg2col["week"]]


def create_features(df: DataFrame, n_feature: int) -> DataFrame:
    """_summary_

    Args:
        df (DataFrame): _description_
        n_feature (int): _description_

    Returns:
        DataFrame: _description_
    """
    return reduce(
        lambda d, i: d.withColumn(
            i, rand((int(i.split("_")[1]) + 1)) * (int(i.split("_")[1]) + 1) * 100.0
        ),
        ["feat_{}".format(c) for c in range(n_feature)],
        df,
    )


def sequence_explode(df: DataFrame) -> DataFrame:
    """_summary_

    Args:
        DF (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_col = "date_from"
    col2logic = {
        "weekofyear": (F.weekofyear(F.col(date_col))).cast(T.IntegerType()),
    }
    date_sequencer = f"sequence(to_date('{2020-12-24}'), to_date('{2023-12-24}'), interval {'1 week'}) AS {date_col}"
    df = df.selectExpr("*", date_sequencer)
    df = df.withColumn(date_col, F.explode(F.col(date_col))).withColumn(PK[-1], col2logic[PK[-1]])
    return df
