from pyspark.sql import SparkSession, Row
import pydeequ
from pydeequ.checks import *
from pydeequ.verification import *

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("PyDeequ Data Quality Checks") \
    .getOrCreate()

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
