import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD DATA
# ==========================================

stockout = pd.read_csv(
    "data/stockout_analysis.csv"
)

inventory = pd.read_csv(
    "data/inventory_recommendations.csv"
)

print("Stockout analysis:", stockout.shape)
print("Inventory recommendations:", inventory.shape)


# ==========================================
# 2. MERGE ALL SKU DATA
# ==========================================

recommendation = stockout.merge(
    inventory[
        [
            "store_id",
            "item_id",
            "average_demand",
            "demand_std",
            "lead_time_demand",
            "safety_stock",
            "reorder_point"
        ]
    ],
    on=["store_id", "item_id"],
    how="left"
)

print("\nMerged data:", recommendation.shape)


# ==========================================
# 3. CALCULATE STOCKOUT SEVERITY
# ==========================================

def calculate_priority(row):

    rate = row["stockout_rate"]
    shortage = row["total_shortage"]

    # Critical
    if rate >= 5 or shortage >= 5000:
        return "Critical"

    # High
    elif rate >= 3 or shortage >= 3000:
        return "High"

    # Medium
    elif rate >= 1 or shortage >= 1000:
        return "Medium"

    # Low
    else:
        return "Low"


recommendation["priority"] = recommendation.apply(
    calculate_priority,
    axis=1
)


# ==========================================
# 4. RECOMMEND ACTION
# ==========================================

def recommend_action(row):

    rate = row["stockout_rate"]
    shortage = row["total_shortage"]

    if rate >= 5 or shortage >= 5000:

        return "Increase reorder quantity and safety stock"

    elif rate >= 3 or shortage >= 3000:

        return "Increase safety stock"

    elif rate >= 1 or shortage >= 1000:

        return "Monitor inventory closely"

    else:

        return "Maintain current inventory policy"


recommendation["recommended_action"] = recommendation.apply(
    recommend_action,
    axis=1
)


# ==========================================
# 5. CALCULATE RECOMMENDED SAFETY STOCK
# ==========================================

recommendation["recommended_safety_stock"] = (
    recommendation["safety_stock"]
)


# Increase safety stock based on severity

recommendation.loc[
    recommendation["priority"] == "Medium",
    "recommended_safety_stock"
] = (
    recommendation.loc[
        recommendation["priority"] == "Medium",
        "safety_stock"
    ] * 1.20
)

recommendation.loc[
    recommendation["priority"] == "High",
    "recommended_safety_stock"
] = (
    recommendation.loc[
        recommendation["priority"] == "High",
        "safety_stock"
    ] * 1.35
)

recommendation.loc[
    recommendation["priority"] == "Critical",
    "recommended_safety_stock"
] = (
    recommendation.loc[
        recommendation["priority"] == "Critical",
        "safety_stock"
    ] * 1.50
)


# ==========================================
# 6. CALCULATE RECOMMENDED REORDER POINT
# ==========================================

recommendation["recommended_reorder_point"] = (
    recommendation["lead_time_demand"]
    + recommendation["recommended_safety_stock"]
)


# ==========================================
# 7. ROUND VALUES
# ==========================================

numeric_columns = [
    "average_demand",
    "demand_std",
    "lead_time_demand",
    "safety_stock",
    "reorder_point",
    "total_shortage",
    "stockout_rate",
    "recommended_safety_stock",
    "recommended_reorder_point"
]

for column in numeric_columns:

    if column in recommendation.columns:

        recommendation[column] = recommendation[column].round(2)


# ==========================================
# 8. SELECT FINAL COLUMNS
# ==========================================

final_columns = [
    "store_id",
    "item_id",

    "average_demand",
    "demand_std",
    "lead_time_demand",

    "safety_stock",
    "reorder_point",

    "stockout_days",
    "total_shortage",
    "total_demand",
    "stockout_rate",

    "recommended_safety_stock",
    "recommended_reorder_point",

    "priority",
    "recommended_action"
]

recommendation = recommendation[final_columns]


# ==========================================
# 9. SAVE RESULTS
# ==========================================

output_file = (
    "data/inventory_recommendations_final.csv"
)

recommendation.to_csv(
    output_file,
    index=False
)


# ==========================================
# 10. DISPLAY SUMMARY
# ==========================================

print("\n=================================")
print("INVENTORY RECOMMENDATION SUMMARY")
print("=================================")

print(
    "\nTotal SKUs:",
    len(recommendation)
)

print(
    "\nPriority distribution:"
)

print(
    recommendation["priority"].value_counts()
)

print(
    "\nRecommended actions:"
)

print(
    recommendation["recommended_action"].value_counts()
)


print("\n=================================")
print("TOP 10 CRITICAL SKUs")
print("=================================")

print(
    recommendation[
        recommendation["priority"] == "Critical"
    ]
    .sort_values(
        "total_shortage",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)


print("\n=================================")
print("RECOMMENDATION COMPLETED")
print("=================================")

print(
    "Saved to:",
    output_file
)
