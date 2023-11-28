import os


# Set the environment variable for Spark version
os.environ['SPARK_VERSION'] = '3.3'

# Now import PySpark and PyDeequ modules
from pyspark.sql import SparkSession, Row
import pydeequ

import os

# Set the environment variable for Spark version
os.environ['SPARK_VERSION'] = '3.3'


spark = SparkSession.builder.appName("PyDeequ Test").getOrCreate()
print("Using Spark Version:", spark.version)

from py4j.java_gateway import java_import
java_import(spark._sc._jvm, "org.apache.spark.sql.api.python.*")

# Ensure this prints 3.3.x

from pydeequ.checks import *
from pydeequ.verification import *

# Hardcoded data
data = spark.createDataFrame([
    Row(UserID=1, UserName="Alice", Email="alice@example.com", SignUpDate=20200101),
    Row(UserID=2, UserName="Bob", Email="bob@example.com", SignUpDate=20200102),
    Row(UserID=3, UserName="Charlie", Email="charlie@example.com", SignUpDate=20200103),
    # Add more rows as needed
])

# Define the checks you want to perform
check = Check(spark, CheckLevel.Error, "Data Quality Checks")

checkResult = VerificationSuite(spark) \
    .onData(data) \
    .addCheck(
        check.hasSize(lambda x: x >= 3)  # Check if the dataset has at least 3 rows
        .isComplete("UserID")  # Check if 'UserID' column has no nulls
        .isUnique("UserID")  # Check if 'UserID' column values are unique
        # Add more checks as needed
    ) \
    .run()

# Output the results
if checkResult.status == "Success":
    print("Data quality check passed!")
else:
    print("Data quality check failed!")
    for check, result in checkResult.checkResults.items():
        print(f"{result.constraint}: {result.status}")

spark.stop()



