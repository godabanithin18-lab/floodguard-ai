import joblib
import pandas as pd

model = joblib.load("flood_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

coefficients = pd.Series(model.coef_, index=feature_columns)
coefficients_sorted = coefficients.sort_values(ascending=False)

print("=" * 50)
print("MODEL: Linear Regression")
print(f"Intercept (base risk): {model.intercept_:.6f}")
print("=" * 50)
print("\nFACTOR WEIGHTS (contribution to Flood Probability):")
print(coefficients_sorted)
print("=" * 50)

# Sanity check with a manual prediction
sample = pd.DataFrame([[5]*20], columns=feature_columns)  # all factors at moderate level 5
prediction = model.predict(sample)[0]
print(f"\nSample prediction (all factors = 5): {prediction:.4f}")