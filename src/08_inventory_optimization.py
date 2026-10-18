import pandas as pd
from scipy.stats import norm

# Load processed dataset
df = pd.read_csv("data/processed_retail_sales.csv")

df["date"] = pd.to_datetime(df["date"])

print("Dataset shape:", df.shape)

# ---------------------------------
# Inventory Parameters
# ---------------------------------

lead_time = 5
service_level = 0.95

# Calculate Z-score
z_score = norm.ppf(service_level)

print("Lead Time:", lead_time, "days")
print("Service Level:", service_level * 100, "%")
print("Z-score:", round(z_score, 3))


# ---------------------------------
# Calculate Inventory Metrics
# for every Store + Item
# ---------------------------------

inventory = (
    df.groupby(["store_id", "item_id"])["sales"]
      .agg(
          average_demand="mean",
          demand_std="std"
      )
      .reset_index()
)


# ---------------------------------
# Lead-Time Demand
# ---------------------------------

inventory["lead_time_demand"] = (
    inventory["average_demand"] * lead_time
)


# ---------------------------------
# Safety Stock
# ---------------------------------

inventory["safety_stock"] = (
    z_score
    * inventory["demand_std"]
    * (lead_time ** 0.5)
)


# ---------------------------------
# Reorder Point
# ---------------------------------

inventory["reorder_point"] = (
    inventory["lead_time_demand"]
    + inventory["safety_stock"]
)


# Round values
inventory["average_demand"] = inventory["average_demand"].round(2)
inventory["demand_std"] = inventory["demand_std"].round(2)
inventory["lead_time_demand"] = inventory["lead_time_demand"].round(2)
inventory["safety_stock"] = inventory["safety_stock"].round(2)
inventory["reorder_point"] = inventory["reorder_point"].round(2)


# ---------------------------------
# Display Results
# ---------------------------------

print("\nInventory Recommendations:")
print(inventory.head(10))

print("\nTotal Store-Item combinations:", len(inventory))


# ---------------------------------
# Save Results
# ---------------------------------

inventory.to_csv(
    "data/inventory_recommendations.csv",
    index=False
)

print("\nInventory recommendations saved successfully!")
