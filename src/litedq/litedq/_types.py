# Import
from collections import namedtuple
from pandas import DataFrame as PandasDataFrame
from pyspark.sql import DataFrame as SparkDataFrame
from typing import NewType, Callable, Union, Tuple, Dict


# Define new types
DataInput = NewType("DataInput", Union[PandasDataFrame, SparkDataFrame])
DataOutput = NewType("DataOutput", Tuple[Union[Dict, None], bool])
Question = namedtuple("Question", "func desc app_handler")
Application = namedtuple("Application", "data metadata")
QuestionFunction = Callable[[DataInput], DataOutput]
