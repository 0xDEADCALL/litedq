from setuptools import setup

VERSION = "0.2"
DESCRIPTION = "Light data quality library"
LONG_DESCRIPTION = """
    lite-dq enables the user to define and execute simple "data quality" checks
    as well as complex business logic, thus we introduce the concept of "Question"
    "Application" and "Subject".
        - Question: check over any arbitrary transformation whether a conditions is met.
        - Application: perform the check defined as a "Question" over any compatible data asset.
        - Subject: relevant bit of data over which the questions is performed (i.e a dataframe with the
                   metric calculation for a given group). Can be specified or not.
"""

setup(
    name="litedq",
    version="0.2",
    author="Alexandru-Vasile Stirban",
    author_email="stirban@pm.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["litedq"],
    python_requites=">=3.9",
    install_requires=[
        "pandas",
        "pyspark"
    ],
)
