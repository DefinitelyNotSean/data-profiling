from pyspark.sql import SparkSession
import great_expectations as ge

# Initialize a Spark session
spark = SparkSession.builder.appName("DataQualityChecks").getOrCreate()

# Read your Parquet file
df = spark.read.parquet("path_to_your_parquet_file")

# Convert to a Great Expectations Dataset
ge_df = ge.dataset.SparkDFDataset(df)

# Define your expectations
ge_df.expect_column_values_to_match_regex('busApp', '^ASV.*')
ge_df.expect_column_values_to_be_in_set('ResTier', ['Gold', 'Silver', 'Platinum'])
ge_df.expect_column_values_to_be_in_set('CompletedTests', [0, 1])
ge_df.expect_column_values_to_be_in_set('TestStatus', [0, 1])
ge_df.expect_column_values_to_be_between('Year', 1000, 9999)
ge_df.expect_column_values_to_match_regex('SnapDt', r'\d{4}-\d{2}-\d{2}')

# Run validation
results = ge_df.validate()

# Print the results
print(results)

# Stop the Spark session
spark.stop()
