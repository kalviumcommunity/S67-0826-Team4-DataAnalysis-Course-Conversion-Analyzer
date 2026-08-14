import pandas as pd

df = pd.read_csv("data/courses.csv")

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATASET SIZE ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
print(df.dtypes)