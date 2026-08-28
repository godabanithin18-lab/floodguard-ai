import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("flood.csv")
if "id" in df.columns:
    df = df.drop("id", axis=1)

X = df.drop("FloodProbability", axis=1)
y = df["FloodProbability"]
feature_columns = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Try multiple models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=4, random_state=42)
}

results = {}
best_model = None
best_r2 = -999
best_name = ""

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    results[name] = r2
    print(f"{name}: R² = {r2:.4f}, MAE = {mae:.4f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_name = name

print("=" * 50)
print(f"BEST MODEL: {best_name} with R² = {best_r2:.4f}")
print("=" * 50)

# Save the best model
joblib.dump(best_model, "flood_model.pkl")
joblib.dump(feature_columns, "feature_columns.pkl")
joblib.dump(best_name, "model_name.pkl")

print(f"\n✅ Saved best model ({best_name}) successfully!")