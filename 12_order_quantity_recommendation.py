import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD RECOMMENDATION DATA
# ==========================================

df = pd.read_csv(
    "data/inventory_recommendations_final.csv"
)

print("Recommendation data:", df.shape)


# ==========================================
# 2. CALCULATE RECOMMENDED ORDER QUANTITY
# ==========================================

# Base order quantity = average demand × lead-time coverage
#
# We use the lead-time demand as the base
# and adjust the quantity according to priority.

df["base_order_quantity"] = df["average_demand"] * 5


# ==========================================
# 3. PRIORITY-BASED ORDER ADJUSTMENT
# ==========================================

def calculate_order_quantity(row):

    base_quantity = row["base_order_quantity"]

    if row["priority"] == "Critical":

        # Higher quantity for critical SKUs
        quantity = base_quantity * 1.50

    elif row["priority"] == "High":

        quantity = base_quantity * 1.30

    elif row["priority"] == "Medium":

        quantity = base_quantity * 1.15

    else:

        quantity = base_quantity

    return quantity


df["recommended_order_quantity"] = df.apply(
    calculate_order_quantity,
    axis=1
)


# ==========================================
# 4. ROUND ORDER QUANTITY
# ==========================================

df["recommended_order_quantity"] = (
    np.ceil(
        df["recommended_order_quantity"]
    )
    .astype(int)
)


# ==========================================
# 5. UPDATE ACTION
# ==========================================

def update_action(row):

    if row["priority"] == "Critical":

        return (
            "Urgent reorder - increase safety stock "
            "and order recommended quantity"
        )

    elif row["priority"] == "High":

        return (
            "Increase safety stock and "
            "order recommended quantity"
        )

    elif row["priority"] == "Medium":

        return (
            "Monitor inventory and "
            "order recommended quantity"
        )

    else:

        return "Maintain current inventory policy"


df["recommended_action"] = df.apply(
    update_action,
    axis=1
)


# ==========================================
# 6. REMOVE TEMPORARY COLUMN
# ==========================================

df.drop(
    columns=["base_order_quantity"],
    inplace=True
)


# ==========================================
# 7. SAVE FINAL RECOMMENDATIONS
# ==========================================

output_file = (
    "data/final_inventory_recommendations.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n=================================")
print("ORDER QUANTITY RECOMMENDATION")
print("=================================")

print(
    "Total SKUs:",
    len(df)
)

print(
    "\nPriority distribution:"
)

print(
    df["priority"].value_counts()
)


print("\n=================================")
print("TOP 10 CRITICAL SKUs")
print("=================================")

critical = df[
    df["priority"] == "Critical"
].sort_values(
    "recommended_order_quantity",
    ascending=False
)

print(
    critical[
        [
            "store_id",
            "item_id",
            "average_demand",
            "stockout_rate",
            "total_shortage",
            "priority",
            "recommended_safety_stock",
            "recommended_reorder_point",
            "recommended_order_quantity",
            "recommended_action"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ==========================================
# 9. COMPLETION
# ==========================================

print("\n=================================")
print("ORDER QUANTITY CALCULATION COMPLETED")
print("=================================")

print(
    "Saved to:",
    output_file
)