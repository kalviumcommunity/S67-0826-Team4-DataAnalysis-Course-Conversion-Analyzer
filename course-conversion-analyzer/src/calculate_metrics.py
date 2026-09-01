import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_courses.csv")

print(df.head())

# Keep metric scale consistent with the analysis/dashboard pipeline: ratios, not percentages.
views = df["views"].astype(float).replace(0, float("nan"))
preview_clicks = df["preview_clicks"].astype(float).replace(0, float("nan"))

# Calculate conversion rate as a ratio
df["conversion_rate"] = (df["enrollments"] / views).round(4)

# Calculate preview-to-enrollment conversion as a ratio
df["preview_conversion"] = (df["enrollments"] / preview_clicks).round(4)

# Calculate benchmarks
median_views = df["views"].median()
median_conversion = df["conversion_rate"].median()

print("Median views:", round(median_views, 2))
print("Median conversion:", round(median_conversion, 4))