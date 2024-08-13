class QuestionAlreadyExists(Exception):
    """
    Raised when two functions/questions
    are registered under the same id
    """

    def __init__(self, id: str):
        super().__init__(f"Question with id ({id}) has already been registered")


class QuestionHasNotBeenRegistered(Exception):
    """
    Raised when application is performed and the question
    hasn't been registered
    """

    def __init__(self, id: str):
        super().__init__(f"ID ({id}) is not registered as a question")


class SparkSessionNotProvided(Exception):
    """
    Raised when application is performed and the question
    hasn't been registered
    """

    def __init__(self):
        super().__init__(
            f"Spark export method has been selected but no spark session has ben provided"
        )


class FunctionAlreadyRegistered(Exception):
    """
    Raised when the same function name has already been
    registered
    """

    def __init__(self, name: str):
        super().__init__(f"{name} function has already been registered")


class UnknownExportMethod(Exception):
    """
    Raised when the export method is unknow
    when running the questions
    """

    def __init__(self, export: str):
        super().__init__(f'Export method "{export}" is not a valid option')


class DataIsNotDataframe(Exception):
    """
    Raised when the provided data for a given question
    is not a dataframe
    """

    def __init__(self, data: any):
        super().__init__(f"{type(data)} is not a valid input parameter")
