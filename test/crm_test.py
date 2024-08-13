from pathlib import Path

import pandas as pd
from rich import print
from pyspark.sql import SparkSession
from questions import *

from litedq import DataQuestions as dq

# Current Path
file_path = Path(__file__)
data_path = file_path.parent / "data"

# Get spark sessions
spark = SparkSession.builder.appName(file_path.stem).getOrCreate()

# Read data as spark
sales_df = spark.read.option("header", True).csv(str(data_path / "sales_pipeline.csv"))
accounts_df = spark.read.option("header", True).csv(str(data_path / "accounts.csv"))

# Read data as pandas
sales_pd = pd.read_csv(data_path / "sales_pipeline.csv")
accounts_pd = pd.read_csv(data_path / "accounts.csv")

# Check we have all the questions
print(dq.questions)

# Add application
dq["check_countries_df"].apply(accounts_df=accounts_df, spark=spark)
dq["check_dates_df"].apply(accounts_df=accounts_df, sales_df=sales_df, spark=spark)

# Check we have application
print(dq["check_countries_df"])
print(dq["check_dates_df"])

# Execute
print(dq.run())
