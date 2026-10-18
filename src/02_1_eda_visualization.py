import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/retail_sales.csv")

# ----------------------------
# Total Sales by Month
# ----------------------------
#monthly_sales = df.groupby("month")["sales"].sum()

#plt.figure(figsize=(10,5))
#monthly_sales.plot(kind="bar")
#plt.title("Monthly Sales")
#plt.xlabel("Month")
#plt.ylabel("Total Sales")
#plt.tight_layout()
#plt.show()

# ----------------------------
# Sales by Weekday
# ----------------------------
#weekday_sales = df.groupby("weekday")["sales"].sum()

#plt.figure(figsize=(8,5))
#weekday_sales.plot(kind="bar")
#plt.title("Weekday Sales")
#plt.xlabel("Weekday")
#plt.ylabel("Total Sales")
#plt.tight_layout()
#plt.show()

# ----------------------------
# Top 10 Stores
# ----------------------------
#top_stores = df.groupby("store_id")["sales"].sum().sort_values(ascending=False).head(10)

#plt.figure(figsize=(10,5))
#top_stores.plot(kind="bar")
#plt.title("Top 10 Stores by Sales")
#plt.xlabel("Store ID")
#plt.ylabel("Total Sales")
#plt.tight_layout()
#plt.show()

# ----------------------------
# Top 10 Items
# ----------------------------
#top_items = df.groupby("item_id")["sales"].sum().sort_values(ascending=False).head(10)

#plt.figure(figsize=(10,5))
#top_items.plot(kind="bar")
#plt.title("Top 10 Items by Sales")
#plt.xlabel("Item ID")
#plt.ylabel("Total Sales")
#plt.tight_layout()
#plt.show()

# ----------------------------
# Promotion Effect
# ----------------------------
promo_sales = df.groupby("promo")["sales"].mean()

#plt.figure(figsize=(6,5))
#promo_sales.plot(kind="bar")
#plt.title("Average Sales: Promotion vs No Promotion")
#plt.xlabel("Promotion")
#plt.ylabel("Average Sales")
#plt.tight_layout()
#plt.show()

# ----------------------------
# Price Distribution
# ----------------------------
plt.figure(figsize=(8,5))
plt.hist(df["price"], bins=30)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
