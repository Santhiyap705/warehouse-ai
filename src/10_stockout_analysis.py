import pandas as pd

# ---------------------------------
# Load Simulation Results
# ---------------------------------

df = pd.read_csv(
    "data/inventory_simulation_results.csv"
)

df["date"] = pd.to_datetime(df["date"])

print("Simulation data:", df.shape)


# ---------------------------------
# 1. Overall Stockout Summary
# ---------------------------------

total_days = len(df)

stockout_days = df["stockout"].sum()

total_shortage = df["shortage"].sum()

stockout_rate = (stockout_days / total_days) * 100

print("\n=================================")
print("OVERALL STOCKOUT ANALYSIS")
print("=================================")

print("Total simulation records:", total_days)
print("Total stockout days:", stockout_days)
print("Total shortage units:", total_shortage)
print("Stockout rate:", round(stockout_rate, 2), "%")


# ---------------------------------
# 2. Stockout Analysis by SKU
# ---------------------------------

sku_analysis = (
    df.groupby(["store_id", "item_id"])
    .agg(
        total_days=("date", "count"),
        stockout_days=("stockout", "sum"),
        total_shortage=("shortage", "sum"),
        total_demand=("demand", "sum")
    )
    .reset_index()
)


# ---------------------------------
# 3. Calculate Stockout Rate
# ---------------------------------

sku_analysis["stockout_rate"] = (
    sku_analysis["stockout_days"]
    / sku_analysis["total_days"]
) * 100


# ---------------------------------
# 4. Sort by Most Stockouts
# ---------------------------------

sku_analysis = sku_analysis.sort_values(
    "stockout_days",
    ascending=False
)


print("\n=================================")
print("TOP 10 SKUs WITH MOST STOCKOUTS")
print("=================================")

print(
    sku_analysis.head(10)
)


# ---------------------------------
# 5. Top 10 SKUs by Shortage
# ---------------------------------

top_shortage = sku_analysis.sort_values(
    "total_shortage",
    ascending=False
)

print("\n=================================")
print("TOP 10 SKUs BY SHORTAGE")
print("=================================")

print(
    top_shortage[
        [
            "store_id",
            "item_id",
            "stockout_days",
            "total_shortage",
            "stockout_rate"
        ]
    ].head(10)
)


# ---------------------------------
# 6. Save Analysis
# ---------------------------------

sku_analysis.to_csv(
    "data/stockout_analysis.csv",
    index=False
)

print("\n=================================")
print("ANALYSIS COMPLETED")
print("=================================")

print(
    "Saved to: data/stockout_analysis.csv"
)
