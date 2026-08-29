import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv("flood.csv")
if "id" in df.columns:
    df = df.drop("id", axis=1)

X = df.drop("FloodProbability", axis=1)
y = df["FloodProbability"]

print(f"Dataset size: {len(df)} samples")
print(f"Number of features: {X.shape[1]}")
print(f"Features: {X.columns.tolist()}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print("=" * 60)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=4, random_state=42),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    print(f"\n{name}")
    print(f"  R² Score: {r2:.4f}")
    print(f"  MAE:      {mae:.5f}")
    print(f"  RMSE:     {rmse:.5f}")

print("=" * 60)

# Coefficient analysis for Linear Regression (justification)
lr = models["Linear Regression"]
coef_df = pd.Series(lr.coef_, index=X.columns).sort_values(ascending=False)
print("\nLinear Regression Coefficients (feature contribution weights):")
print(coef_df)
print(f"\nIntercept: {lr.intercept_:.6f}")