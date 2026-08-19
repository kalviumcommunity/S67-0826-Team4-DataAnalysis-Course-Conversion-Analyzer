import pandas as pd

df = pd.read_csv("data/courses.csv")

print("Original dataset:")
print(df)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("\nMissing values before cleaning:")
print(df.isnull().sum())