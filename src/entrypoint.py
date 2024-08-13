import sys

from pyspark.context import SparkContext
from awsglue.context import GlueContext

from awsglue.utils import getResolvedOptions
from logic import Executor

# Bring question definition into current context
from questions import *

# Init glue
sc = SparkContext.getOrCreate()
glue_ctx = GlueContext(sc)
spark = glue_ctx.spark_session

# Get arguments
args = getResolvedOptions(sys.argv,[
    "target_bucket",
    "target_database",
    "target_table",
    "write_mode",
    "dry_run"
])

# Init custom executor
Executor(args, spark, glue_ctx)._run(dry_run=True if args["dry_run"] == "true" else False)

