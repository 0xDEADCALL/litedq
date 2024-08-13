import json

from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit

from litedq import DataQuestions as dq


@dq.register("check_sectors_df", "Check all the required sectors are present")
def check_sectors_df(accounts_df, spark):
    data = [
        "finance",
        "technolgy",
        "software",
        "marketing",
        "retail",
        "services",
        "entertainment",
        "telecommunications",
        "employment",
        "medical",
        "automotive",
    ]

    truth_df = spark.createDataFrame([{"sector": x} for x in data])

    df = (
        accounts_df.select("sector")
        .distinct()
        .join(truth_df, on="sector", how="full")
        .withColumn(
            "missing", F.when(accounts_df.sector.isNull(), True).otherwise(False)
        )
    )

    subject = json.dumps(df.toPandas().to_dict(orient="records"))
    sec_check = df.filter("missing = TRUE").count() == 0

    return subject, sec_check


@dq.register("check_countries_df", "Check all the countries are present")
def check_countries_df(accounts_df, spark):
    df = accounts_df.select("office_location").distinct()

    subject = json.dumps(df.toPandas().to_dict(orient="records"))
    loc_check = df.count() == 15

    return subject, loc_check


@dq.register("check_dates_df", "Check the maximum and minimum dates for each location")
def check_dates_df(accounts_df, sales_df, spark):
    df = (
        sales_df.join(accounts_df, on="account", how="left")
        .filter("office_location IS NOT NULL")
        .groupBy("office_location")
        .agg(
            F.max("engage_date").alias("max_date"),
            F.min("engage_date").alias("min_date"),
        )
        .withColumn(
            "max_date_check",
            F.when(col("max_date") > "2017-12-01", True).otherwise(False),
        )
        .withColumn(
            "min_date_check",
            F.when(col("min_date") < "2016-11-01", True).otherwise(False),
        )
    )

    subject = json.dumps(df.toPandas().to_dict(orient="records"))
    max_check = df.filter("max_date_check == FALSE").count() == 0
    min_check = df.filter("min_date_check == FALSE").count() == 0

    return subject, max_check and min_check
