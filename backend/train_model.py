import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load dataset
df = pd.read_csv("flood_risk_dataset_india.csv")

# Encode categorical columns (Land Cover, Soil Type are text -> convert to numbers)
le_land = LabelEncoder()
le_soil = LabelEncoder()
df["Land Cover"] = le_land.fit_transform(df["Land Cover"])
df["Soil Type"] = le_soil.fit_transform(df["Soil Type"])

# Features (everything except the target) and target
X = df.drop("Flood Occurred", axis=1)
y = df["Flood Occurred"]

feature_columns = X.columns.tolist()
print("Training on features:", feature_columns)

# Split into train/test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("=" * 50)
print(f"ACCURACY: {accuracy * 100:.2f}%")
print("=" * 50)
print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred))
print("=" * 50)
print("\nCONFUSION MATRIX:")
print(confusion_matrix(y_test, y_pred))
print("=" * 50)

# Feature importance (which factors matter most for flood prediction)
importances = pd.Series(model.feature_importances_, index=feature_columns)
print("\nFEATURE IMPORTANCE (most predictive factors):")
print(importances.sort_values(ascending=False))

# Save the model and encoders so the API can use them later
joblib.dump(model, "flood_model.pkl")
joblib.dump(le_land, "land_cover_encoder.pkl")
joblib.dump(le_soil, "soil_type_encoder.pkl")
joblib.dump(feature_columns, "feature_columns.pkl")

print("\n✅ Model and encoders saved successfully!")