import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/Retail_Sales.csv")

# -------------------------------
# Basic Information
# -------------------------------
print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

# -------------------------------
# Total Sales
# -------------------------------
print("\nTotal Sales:", df["sales"].sum())

# -------------------------------
# Store-wise Sales
# -------------------------------
store_sales = df.groupby("store_id")["sales"].sum()
print("\nStore-wise Sales:")
print(store_sales)

# -------------------------------
# Top 10 Selling Items
# -------------------------------
top_items = df.groupby("item_id")["sales"].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Selling Items:")
print(top_items)

# -------------------------------
# Monthly Sales
# -------------------------------
monthly_sales = df.groupby("month")["sales"].sum()

plt.figure(figsize=(8,5))
monthly_sales.plot(kind="bar")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.show()