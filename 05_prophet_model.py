import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error

# Load processed dataset
df = pd.read_csv("data/processed_retail_sales.csv")

# Select one store and one item
sku = df[
    (df["store_id"] == "store_1") &
    (df["item_id"] == "item_1")
].copy()

# Prophet needs columns named ds and y
prophet_df = sku[["date", "sales"]].rename(
    columns={
        "date": "ds",
        "sales": "y"
    }
)

# Convert date
prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

print(prophet_df.head())

# Create Prophet model
model = Prophet()

# Train the model
model.fit(prophet_df)

print("Prophet Model Trained Successfully!")

# Create future dates (next 30 days)
future = model.make_future_dataframe(periods=30)

print(future.tail())

# Generate predictions
forecast = model.predict(future)

# Display important columns
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

# Predict on historical data
historical_forecast = model.predict(prophet_df[["ds"]])

# Add actual sales
historical_forecast["actual"] = prophet_df["y"].values

# Calculate MAE
mae = mean_absolute_error(
    historical_forecast["actual"],
    historical_forecast["yhat"]
)

print("\nProphet MAE:", round(mae, 2))

