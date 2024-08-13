import abc
from litedq import DataQuestions as dq
from pyspark.sql import SparkSession


class BaseExecutor(metaclass=abc.ABCMeta):
    def __init__(self, args, spark, glue_ctx) -> None:
        self.spark = spark
        self.glue_ctx = glue_ctx
        self.target_bucket = args["target_bucket"]
        self.target_database = args["target_database"]
        self.target_table = args["target_table"]
        self.write_mode = args["write_mode"]

    @abc.abstractmethod
    def ask(self) -> None:
        pass

    def _run(self, dry_run = False) -> None:
        # Load applications
        self.ask()

        # Execute questions transformations
        data_df = dq.run("spark", self.spark)

        # Write table
        if not dry_run:
            self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {self.target_database}")
            
            (data_df
                .write
                .mode(self.write_mode)
                .option("path", f"s3://{self.target_bucket}/{self.target_table}")
                .format("parquet")
                .saveAsTable(f"{self.target_database}.{self.target_table}")
            )
