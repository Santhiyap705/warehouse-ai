import pandas as pd

# Load dataset
df = pd.read_csv("data/Retail_Sales.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort data (very important for time series)
df = df.sort_values(["store_id", "item_id", "date"])

# -----------------------------
# Date Features
# -----------------------------
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# -----------------------------
# Lag Features
# -----------------------------
df["lag_1"] = df.groupby(["store_id", "item_id"])["sales"].shift(1)
df["lag_7"] = df.groupby(["store_id", "item_id"])["sales"].shift(7)
df["lag_30"] = df.groupby(["store_id", "item_id"])["sales"].shift(30)

# -----------------------------
# Rolling Mean Features
# -----------------------------
df["rolling_mean_7"] = (
    df.groupby(["store_id", "item_id"])["sales"]
      .transform(lambda x: x.shift(1).rolling(7).mean())
)

df["rolling_mean_30"] = (
    df.groupby(["store_id", "item_id"])["sales"]
      .transform(lambda x: x.shift(1).rolling(30).mean())
)

# Remove rows with NaN values created by lag features
df = df.dropna()

# Save processed data
df.to_csv("data/processed_retail_sales.csv", index=False)

print("Feature Engineering Completed Successfully!")
print("New Dataset Shape:", df.shape)
print(df.head())