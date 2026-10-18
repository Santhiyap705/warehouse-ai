import pandas as pd

# ---------------------------------
# Load Data
# ---------------------------------

df = pd.read_csv("data/processed_retail_sales.csv")
inventory = pd.read_csv("data/inventory_recommendations.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

print("Sales data:", df.shape)
print("Inventory data:", inventory.shape)


# ---------------------------------
# Store results for ALL SKUs
# ---------------------------------

all_simulation_results = []


# ---------------------------------
# Run simulation for ALL SKUs
# ---------------------------------

for (store, item), sku_sales in df.groupby(["store_id", "item_id"]):

    # Sort by date
    sku_sales = sku_sales.sort_values("date").copy()

    # Get inventory parameters for this SKU
    sku_inventory_data = inventory[
        (inventory["store_id"] == store) &
        (inventory["item_id"] == item)
    ]

    # Skip if inventory parameters are not available
    if sku_inventory_data.empty:
        continue

    sku_inventory = sku_inventory_data.iloc[0]

    reorder_point = sku_inventory["reorder_point"]

    initial_inventory = 500
    lead_time = 5

    print("\n---------------------------------")
    print("SKU:", store, item)
    print("Number of sales records:", len(sku_sales))
    print("Reorder Point:", reorder_point)
    print("Initial Inventory:", initial_inventory)
    print("Lead Time:", lead_time, "days")
    print("---------------------------------")


    # ---------------------------------
    # Simulation Variables
    # ---------------------------------

    current_inventory = initial_inventory

    pending_orders = []

    stockout_days = 0
    total_stockout_units = 0
    orders_placed = 0

    simulation_results = []


    # ---------------------------------
    # Daily Inventory Simulation
    # ---------------------------------

    for _, row in sku_sales.iterrows():

        date = row["date"]
        demand = row["sales"]

        # Opening inventory
        opening_inventory = current_inventory


        # ---------------------------------
        # Check arriving orders
        # ---------------------------------

        arrived_quantity = 0

        arriving_orders = [
            order for order in pending_orders
            if order["arrival_date"] == date
        ]

        for order in arriving_orders:

            current_inventory += order["quantity"]

            arrived_quantity += order["quantity"]


        # Remove arrived orders

        pending_orders = [
            order for order in pending_orders
            if order["arrival_date"] != date
        ]


        # ---------------------------------
        # Fulfill Demand
        # ---------------------------------

        stockout = 0
        shortage = 0

        if current_inventory >= demand:

            current_inventory -= demand

        else:

            shortage = demand - current_inventory

            total_stockout_units += shortage
            stockout_days += 1
            stockout = 1

            current_inventory = 0


        # ---------------------------------
        # Reorder Decision
        # ---------------------------------

        order_quantity = 0

        if current_inventory <= reorder_point:

            # Only place a new order if
            # there is no pending order

            if len(pending_orders) == 0:

                order_quantity = 300

                arrival_date = (
                    date + pd.Timedelta(days=lead_time)
                )

                pending_orders.append({

                    "order_date": date,

                    "arrival_date": arrival_date,

                    "quantity": order_quantity

                })

                orders_placed += 1


        # ---------------------------------
        # Save Daily Result
        # ---------------------------------

        simulation_results.append({

            "date": date,

            "store_id": store,

            "item_id": item,

            "demand": demand,

            "opening_inventory": opening_inventory,

            "arrived_quantity": arrived_quantity,

            "order_placed": order_quantity,

            "closing_inventory": current_inventory,

            "stockout": stockout,

            "shortage": shortage

        })


    # ---------------------------------
    # Add this SKU's results
    # ---------------------------------

    all_simulation_results.extend(simulation_results)


    # ---------------------------------
    # Print SKU Summary
    # ---------------------------------

    print("Stockout Days:", stockout_days)
    print("Total Shortage Units:", total_stockout_units)
    print("Orders Placed:", orders_placed)


# ---------------------------------
# Create Final Results DataFrame
# ---------------------------------

simulation_df = pd.DataFrame(all_simulation_results)


# ---------------------------------
# Save Results
# ---------------------------------

simulation_df.to_csv(
    "data/inventory_simulation_results.csv",
    index=False
)


print("\n=================================")
print("ALL SKU SIMULATION COMPLETED")
print("=================================")


print("Total simulation rows:", len(simulation_df))

print(
    "Total stockout days:",
    simulation_df["stockout"].sum()
)

print(
    "Total shortage units:",
    simulation_df["shortage"].sum()
)

print(
    "Total orders placed:",
    (simulation_df["order_placed"] > 0).sum()
)

print(
    "\nSimulation results saved successfully!"
)

print(
    "File: data/inventory_simulation_results.csv"
)

print("\nExample Shortage Records:")
print(
    simulation_df[
        simulation_df["shortage"] > 0
    ].head(10)
)
