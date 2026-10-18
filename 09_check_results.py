import pandas as pd

file = "data/inventory_simulation_results.csv"

df = pd.read_csv(file)

print("CSV shape:", df.shape)

print("\nStockout records:")
print(
    df[df["stockout"] == 1].head(10)
)

print(
    "\nTotal stockout records:",
    (df["stockout"] == 1).sum()
)

print(
    "Total shortage units:",
    df["shortage"].sum()
)