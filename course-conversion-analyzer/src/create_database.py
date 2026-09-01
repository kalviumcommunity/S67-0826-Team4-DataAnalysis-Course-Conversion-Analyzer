import pandas as pd
import sqlite3


# Load analyzed data
df = pd.read_csv("data/analyzed_courses.csv")

# Canonical Step 6 database for the final analyzed dataset.
# The earlier course_conversion.db remains as an intermediate artifact.
# Create SQLite database
connection = sqlite3.connect("data/courses.db")

# Create courses table
df.to_sql(
    "courses",
    connection,
    if_exists="replace",
    index=False,
)

# Verify
result = pd.read_sql_query(
    "SELECT * FROM courses",
    connection,
)

print(result)

# Close connection
connection.close()

print("\nDatabase created: data/courses.db")