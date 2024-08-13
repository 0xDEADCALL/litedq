# Aux
import json
from datetime import datetime as dt
from uuid import uuid4

from pyspark.sql import SparkSession

from .applicationhandler import ApplicationHanler
from ._const import OUTPUT_SCHEMA
from ._exceptions import *
from ._types import *




# NOTE: magic methods are searched for at class level,
# given that we aren't instantiating DataQuestions it will look for
# the "class" of the "class", which in this case is "type".
# However type.__getitem__ doesn't exist, thus we need to create a metaclass
# that intercepts the lookup and implement the method


class MetaDataQuestions(type):
    def __getitem__(cls, id):
        if id not in cls.questions:
            raise QuestionHasNotBeenRegistered(id)

        return cls.questions[id].app_handler


class DataQuestions(metaclass=MetaDataQuestions):
    questions = {}

    @classmethod
    def register(cls, id: str, desc: str):
        # Exit if multiple questions share the same id
        if id in cls.questions:
            raise QuestionAlreadyExists(id)

        # Make decorator factory
        def decorator(f: QuestionFunction):
            # Check if function with the same name has been registered
            # This should avoid confusions...
            if f.__name__ in [x.func.__name__ for x in cls.questions.values()]:
                raise FunctionAlreadyRegistered(f.__name__)

            # Store question
            cls.questions[id] = Question(f, desc, ApplicationHanler())

            # Store question
            return f

        return decorator

    @classmethod
    def run(cls, output: str = "dict", spark: SparkSession = None):
        # Check export method
        if output not in ("spark", "pandas", "dict"):
            raise UnknownExportMethod()

        # Check attributes
        if output == "spark" and not isinstance(spark, SparkSession):
            raise SparkSessionNotProvided()

        # Get the timestamp per run
        exec_dt = dt.now()

        # Run questions and get results
        results = []

        for id, qst in cls.questions.items():
            for app in qst.app_handler:
                exec = qst.func(**app.data)

                results.append(
                    dict(
                        exec_id=str(uuid4()),
                        exec_dt=exec_dt,
                        question_id=id,
                        question_desc=qst.desc,
                        subject=exec[0],
                        result=exec[1],
                        metadata=json.dumps(app.metadata or "{}"),
                    )
                )

        if output == "spark":
            return spark.createDataFrame(results, schema=OUTPUT_SCHEMA)
        elif output == "pandas":
            return PandasDataFrame.from_records(results)
        else:
            return results
