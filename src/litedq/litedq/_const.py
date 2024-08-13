from pyspark.sql.types import *

# Define the schema of log to be produced
OUTPUT_SCHEMA = StructType(
    [
        StructField("exec_id", StringType()),
        StructField("exec_dt", TimestampType()),
        StructField("question_id", StringType()),
        StructField("question_desc", StringType()),
        StructField("subject", StringType()),
        StructField("result", BooleanType()),
        StructField("metadata", StringType())
    ]
)
