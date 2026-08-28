import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

# Load dataset
df = pd.read_csv("flood.csv")

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Drop 'id' column if present (not a real feature)
if "id" in df.columns:
    df = df.drop("id", axis=1)

# Features and target
X = df.drop("FloodProbability", axis=1)
y = df["FloodProbability"]

feature_columns = X.columns.tolist()
print("\nTraining on features:", feature_columns)

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

print("=" * 50)
print(f"R² SCORE: {r2:.4f}")
print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print("=" * 50)

# Feature importance
importances = pd.Series(model.feature_importances_, index=feature_columns)
print("\nFEATURE IMPORTANCE:")
print(importances.sort_values(ascending=False))

# Save model
joblib.dump(model, "flood_model.pkl")
joblib.dump(feature_columns, "feature_columns.pkl")

print("\n✅ Model and feature list saved successfully!")