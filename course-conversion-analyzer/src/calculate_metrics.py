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

# Identify high-view, low-conversion courses
df["high_view_low_conversion"] = (
    (df["views"] >= median_views) &
    (df["conversion_rate"] <= median_conversion)
)

# Count problematic courses
problem_courses = df["high_view_low_conversion"].sum()
print("High-view, low-conversion courses:", problem_courses)

# Display problematic courses
print("\nHigh-view, low-conversion courses:")
print(
    df[df["high_view_low_conversion"]][
        [
            "course_id",
            "course_name",
            "views",
            "enrollments",
            "conversion_rate",
            "preview_conversion",
        ]
    ]
)

# Save analyzed dataset
df.to_csv("data/analyzed_courses.csv", index=False)

print("\nSaved to: data/analyzed_courses.csv")