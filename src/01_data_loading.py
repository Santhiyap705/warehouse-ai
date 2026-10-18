import pandas as pd

# Load the dataset
df = pd.read_csv("data/Retail_sales.csv")

# Display the first 5 rows
print("First 5 Rows:")
print(df.head())

# Display dataset information
print("\nDataset Information:")
print(df.info())

# Display the shape (rows and columns)
print("\nDataset Shape:")
print(df.shape)

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe())
