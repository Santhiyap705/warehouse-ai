import pandas as pd
import matplotlib.pyplot as plt

# Load the trained model
import joblib

model = joblib.load("models/lightgbm_model.pkl")

# Feature names
features = [
    "lag_1",
    "lag_7",
    "lag_30",
    "rolling_mean_7",
    "rolling_mean_30",
    "price",
    "promo",
    "day_of_week",
    "month",
    "is_weekend"
]

# Get feature importance
importance = model.feature_importances_

# Create a table
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

# Sort from highest to lowest
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance_df)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("LightGBM Feature Importance")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()