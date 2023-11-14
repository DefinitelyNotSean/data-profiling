from pyspark.sql import SparkSession
import spark_df_profiling

# Initialize a Spark session
spark = SparkSession.builder.appName("data_profiling").getOrCreate()

# Load the Parquet data
parquet_file_path = "path_to_your_parquet_file.parquet"
df = spark.read.parquet(parquet_file_path)

# Generate profiling report
profile = spark_df_profiling.ProfileReport(df)
profile.to_file("/path/to/save/report.html")
