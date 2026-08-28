import pandas as pd

# Load the dataset
df = pd.read_csv("flood_risk_dataset_india.csv")

# Basic info
print("=" * 50)
print("SHAPE (rows, columns):", df.shape)
print("=" * 50)
print("\nCOLUMN NAMES:")
print(df.columns.tolist())
print("=" * 50)
print("\nFIRST 5 ROWS:")
print(df.head())
print("=" * 50)
print("\nDATA TYPES:")
print(df.dtypes)
print("=" * 50)
print("\nMISSING VALUES PER COLUMN:")
print(df.isnull().sum())
print("=" * 50)
print("\nBASIC STATISTICS:")
print(df.describe())