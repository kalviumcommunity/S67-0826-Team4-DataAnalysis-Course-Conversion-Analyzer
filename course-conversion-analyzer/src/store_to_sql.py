import sqlite3

import pandas as pd


df = pd.read_csv("data/cleaned_courses.csv")
views = df["views"].astype(float).replace(0, float("nan"))
preview_clicks = df["preview_clicks"].astype(float).replace(0, float("nan"))

df["conversion_rate"] = df["enrollments"] / views
df["preview_to_enrollment_rate"] = df["enrollments"] / preview_clicks

high_view_threshold = df["views"].median()
low_conversion_threshold = df["conversion_rate"].median()

database_path = "data/courses.db"

with sqlite3.connect(database_path) as connection:
    df.to_sql("courses", connection, if_exists="replace", index=False)

    query_course_performance = """
    SELECT
        course_id,
        course_name,
        category,
        price,
        rating,
        views,
        preview_clicks,
        enrollments,
        ROUND(conversion_rate, 4) AS conversion_rate,
        ROUND(preview_to_enrollment_rate, 4) AS preview_to_enrollment_rate
    FROM courses
    ORDER BY conversion_rate DESC;
    """

    query_high_view_low_conversion = """
    SELECT
        course_id,
        course_name,
        category,
        views,
        enrollments,
        ROUND(conversion_rate, 4) AS conversion_rate
    FROM courses
    WHERE views >= ?
    AND conversion_rate <= ?
    ORDER BY views DESC;
    """

    query_category_summary = """
    SELECT
        category,
        COUNT(*) AS course_count,
        ROUND(AVG(price), 2) AS avg_price,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate,
        ROUND(AVG(preview_to_enrollment_rate), 4) AS avg_preview_to_enrollment_rate
    FROM courses
    GROUP BY category
    ORDER BY avg_conversion_rate DESC;
    """

    print("--- COURSE PERFORMANCE QUERY ---")
    print(pd.read_sql_query(query_course_performance, connection))

    print("\n--- HIGH-VIEW / LOW-CONVERSION QUERY ---")
    print(pd.read_sql_query(query_high_view_low_conversion, connection, params=(high_view_threshold, low_conversion_threshold)))

    print("\n--- CATEGORY SUMMARY QUERY ---")
    print(pd.read_sql_query(query_category_summary, connection))

print(f"\nSaved SQLite database to: {database_path}")