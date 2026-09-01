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