import pandas as pd

df = pd.read_csv("data/courses.csv")

print("Original dataset:")
print(df)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Clean text columns before deduplication so whitespace-only differences do not hide duplicates
df["course_id"] = df["course_id"].astype("string").str.strip()
df["course_name"] = df["course_name"].astype("string").str.strip()
df["category"] = df["category"].astype("string").str.strip().str.lower()

# Treat empty strings as missing values
df = df.replace({"course_id": {"": pd.NA}, "course_name": {"": pd.NA}, "category": {"": pd.NA}})

# Remove rows missing essential information
df = df.dropna(subset=["course_id", "course_name", "category"])

# Remove completely duplicated rows
print("\nDuplicates before:", df.duplicated().sum())
df = df.drop_duplicates()

# Remove duplicate course IDs
if df["course_id"].duplicated().sum() > 0:
    df = df.drop_duplicates(subset="course_id", keep="first")

# Standardize categories
category_mapping = {
    "programming": "Programming",
    "data science": "Data Science",
    "web development": "Web Development",
    "business": "Business",
    "design": "Design",
    "marketing": "Marketing",
}
df["category"] = df["category"].replace(category_mapping)