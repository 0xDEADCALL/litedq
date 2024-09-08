<p align="center">
  <img src="docs/assets/LiteDQ.png">
</p>

# Description

> [!WARNING]
> LiteDQ is currently a project under construction.

_LiteDQ_ / _Lite Data Questions_ / _Lite Data Quality_ is small data quality framework that helps implementing
both complex and simple logic checks that aim at monitoring the health of your data assets in AWS.

## Fundamentals

The tool is based on the concept of **Questions**, **Subjects** and **Applications**.
* **Question**: a small unit of code represting the operations needed to perform an arbitrary check over a given asset and table.
* **Subject**: the minimum representation of data over which the check is applied coupled with the global result of the check.
* **Application**: A question and its subject can be reused across different assets, tables or columns, the execution of the same check over different inputsreceives the name of application.

>[!TIP]
> Keep in mind that while using generelized checks is encouraged for a healthier code base, one shouldn't force the over-generalization of a question if there isn't a need for it, thus questions designed for a single application is fine as well.

## Requirements

To be able to deploy the infrastructure the developer we'll need to have a basic understanding and installation of:
* Terraform
* Docker
* AWS VPC
* zip

## Usage

### Question Definition
TBD

### Question Application
TBD

### Entrypoint
TBD

### Deployment
#### Project Structure
TBD

#### Variables
TBD

### Practical Example
First of all, create a new project folder or Git repository and retrieve your AWS credentials to be able to deploy using Terraform. Considering the newly created folder as your working directory:
1. Create a `main.tf` file with the following skeleton:
```terraform
module "dqlogger" {
  source = "https://github.com/0xDEADCALL/litedq"

  // Glue params
  job_name = "dq-data-logger"

  // Bucket variables
  code_repo_bucket = "aws-glue-assets-sample"
  code_path        = "./main.py"
  questions_path   = "./questions"

  // Database name
  target_bucket   = "aws-data-logger-sample"
  target_database = "datalogger"
  target_table    = "logs"

  // Write mode
  write_mode = "append"

  // Don't write anything
  dry_run = false

  // VPC Name
  vpc_name = "litedq-vpc"
}

output "alb_hostname" {
  value = "App Link: ${module.dqlogger.alb_hostname}"
}
```
For more details in the different variables, please see the[Variables](#variables) section.

2. Create a `questions` folder (this can have any name, however we referenced it as this in the previous step in `questions_path`)

3. Define the questions inside python modules in the newly created folder. Any level of subfolders can be used to organize the diferent checks, they will be recursively loaded. As an example, we'll define a check using spark logic inside a `spark` folder

```python
# Spark imports
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit

# Imports related to liteDQ
from litedq import DataQuestions as dq
from litedq import Subject

@dq.register("check_countries_df", "Check all the countries are present")
def check_countries_df(accounts_df, spark):
    df = accounts_df.select("office_location").distinct()
    loc_check = df.count() == 15

    return Subject(loc_check, df)
```
In this case, we're going to check a Spark dataframe has only 15 different countries and return as a subject the countries available as well as the actual result as a boolean.

For more information on how to write checks, please see [Question Definition](#question-definition).

4. Load and preprocess the necessary data inside the `main.py` script
```python
from pyspark.sql.dataframe import DataFrame as sparkDataFrame

# LiteDQ relate imports
from bootstrap import BaseExecutor
from litedq import DataQuestions as dq


# Define entrypoint
class Executor(BaseExecutor):
    def ask(self):
        # Load the by reading from a bucket
        S3_SOURCE = "s3://your-s3-bucket"

        # Retrieve data
        accounts_df: sparkDataFrame = (self.spark.read
            .option("header", True)
            .option("inferSchema", "true")
            .csv(f"{S3_SOURCE}/accounts.csv")
        )

        # Load the data using spark SQL
        # accounts_df = spark.sqk("SELECT * FROM yourdatabase.accounts")
      
        # Apply the check you've defined previously using the "ID"
        dq["check_countries_df"].apply(accounts_df=accounts_df, spark=self.spark)

```

5. Run `terraform apply` and accept the changes.
6. Visit the link provided as output to test the dashboard.


## Technical Implementation

![](docs/assets/infra_diagram.png)

TBD

