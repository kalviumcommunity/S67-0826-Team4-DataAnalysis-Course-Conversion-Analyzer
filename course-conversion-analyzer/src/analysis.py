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