import pandas as pd
from sklearn.metrics import mean_absolute_error

# Load processed data
df = pd.read_csv("data/processed_retail_sales.csv")

# Baseline prediction = yesterday's sales
df["prediction"] = df["lag_1"]

# Remove missing values
df = df.dropna(subset=["prediction"])

# Calculate MAE
mae = mean_absolute_error(df["sales"], df["prediction"])

print("Baseline Model")
print("----------------")
print("Mean Absolute Error (MAE):", round(mae, 2))

# Display a few predictions
print("\nSample Predictions:")
print(df[["date", "sales", "prediction"]].head(10))