import numpy as np
import pandas as pd

df = pd.read_csv("data/analyzed_courses.csv")

print(df)

print(
    df[
        [
            "course_name",
            "category",
            "price",
            "rating",
            "views",
            "preview_clicks",
            "enrollments",
            "conversion_rate",
            "preview_conversion",
            "high_view_low_conversion",
        ]
    ]
)

most_viewed = df.sort_values("views", ascending=False)
print("\n--- MOST VIEWED COURSES ---")
print(most_viewed[["course_name", "views", "enrollments", "conversion_rate"]])

lowest_conversion = df.sort_values("conversion_rate", ascending=True)
print("\n--- LOWEST CONVERSION COURSES ---")
print(lowest_conversion[["course_name", "views", "enrollments", "conversion_rate"]])

problem_courses = df[df["high_view_low_conversion"]]
other_courses = df[~df["high_view_low_conversion"]]

print("\n--- HIGH-VIEW / LOW-CONVERSION COURSES ---")
print(
    problem_courses[
        [
            "course_name",
            "category",
            "price",
            "rating",
            "views",
            "preview_clicks",
            "enrollments",
            "conversion_rate",
            "preview_conversion",
        ]
    ]
)

comparison = pd.DataFrame(
    {
        "Problem Courses": problem_courses[
            [
                "price",
                "rating",
                "views",
                "preview_clicks",
                "preview_conversion",
                "conversion_rate",
            ]
        ].mean(),
        "Other Courses": other_courses[
            [
                "price",
                "rating",
                "views",
                "preview_clicks",
                "preview_conversion",
                "conversion_rate",
            ]
        ].mean(),
    }
)

print("\n--- PROBLEM COURSES VS OTHER COURSES ---")
print(comparison)

category_analysis = df.groupby("category").agg(
    average_views=("views", "mean"),
    average_conversion=("conversion_rate", "mean"),
    average_price=("price", "mean"),
    average_rating=("rating", "mean"),
    course_count=("course_name", "count"),
)

print("\n--- CATEGORY ANALYSIS ---")
print(category_analysis)

problem_avg = problem_courses["conversion_rate"].mean()
other_avg = other_courses["conversion_rate"].mean()
conversion_difference = np.round(other_avg - problem_avg, 4)

print("\nConversion difference:", conversion_difference)