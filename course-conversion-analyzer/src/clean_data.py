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

# Convert numeric columns
numeric_columns = ["price", "rating", "views", "preview_clicks", "enrollments"]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Fill missing numeric values with the median of each column
for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Fix invalid prices
price_median = df.loc[df["price"] >= 0, "price"].median()
df.loc[df["price"] < 0, "price"] = price_median

# Fix invalid ratings
rating_median = df.loc[df["rating"].between(1, 5), "rating"].median()
invalid_ratings = ~df["rating"].between(1, 5)
df.loc[invalid_ratings, "rating"] = rating_median

# Fix invalid views
views_median = df.loc[df["views"] >= 0, "views"].median()
df.loc[df["views"] < 0, "views"] = views_median

# Fix invalid preview clicks
df.loc[df["preview_clicks"] < 0, "preview_clicks"] = 0
df["preview_clicks"] = df[["preview_clicks", "views"]].min(axis=1)

# Fix invalid enrollments
df.loc[df["enrollments"] < 0, "enrollments"] = 0
df["enrollments"] = df[["enrollments", "preview_clicks"]].min(axis=1)