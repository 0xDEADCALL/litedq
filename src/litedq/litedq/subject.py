from ._types import DataInput
from ._exceptions import InvalidDataframeFormat

from pandas import DataFrame as pandasDataframe
from pyspark.sql import DataFrame as sparkDataframe

class Subject:
    def __init__(self, result: bool, df: DataInput = None):
        self.result = result

        if df is not None:
            if isinstance(df, pandasDataframe):
                self.data = df.to_dict(orient="records")
            elif isinstance(df, sparkDataframe):
                self.data = df.toPandas().to_dict(orient="records")
            else:
                raise InvalidDataframeFormat(df)
        else:
            self.data = None
        