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

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print("Duplicates:", df.duplicated().sum())

print("\n--- UNIQUE COURSE IDs ---")
print("Unique IDs:", df["course_id"].nunique())

print("\n--- INVALID RATINGS ---")
print(df[(df["rating"] < 1) | (df["rating"] > 5)])

print("\n--- NEGATIVE PRICES ---")
print(df[df["price"] < 0])

print("\n--- NEGATIVE VIEWS ---")
print(df[df["views"] < 0])

print("\n--- PREVIEW CLICKS > VIEWS ---")
print(df[df["preview_clicks"] > df["views"]])

print("\n--- ENROLLMENTS > PREVIEW CLICKS ---")
print(df[df["enrollments"] > df["preview_clicks"]])

print("\n--- STATISTICAL SUMMARY ---")
print(df.describe())