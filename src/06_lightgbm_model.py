import pandas as pd

# Machine Learning
from lightgbm import LGBMRegressor

# Evaluation
from sklearn.metrics import mean_absolute_error

# Load processed dataset
df = pd.read_csv("data/processed_retail_sales.csv")

print(df.head())
print(df.shape)

# -------------------------
# Select Features
# -------------------------

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

X = df[features]

y = df["sales"]

print("Features Shape:", X.shape)
print("Target Shape:", y.shape)

# -------------------------
# Train-Test Split
# -------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# -------------------------
# Train LightGBM Model
# -------------------------

model = LGBMRegressor(
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)

print("LightGBM Model Trained Successfully!")

# Save the trained model
import joblib

joblib.dump(model, "models/lightgbm_model.pkl")

print("Model saved successfully!")
# -------------------------
# Make Predictions
# -------------------------

predictions = model.predict(X_test)

print("Sample Predictions:")
print(predictions[:10])

# -------------------------
# Evaluate Model
# -------------------------

mae = mean_absolute_error(y_test, predictions)

print("LightGBM MAE:", round(mae, 2))
