import pandas as pd
from dora import DataExplorer

# Load your Parquet file into a Pandas DataFrame
df = pd.read_parquet('/path/to/your/file.parquet')

# Initialize the Data Explorer
explorer = DataExplorer()

# Profile your data
report = explorer.profile(df)

# Display the report
# The report is a dictionary, so you can explore or print it as you like
print(report)
