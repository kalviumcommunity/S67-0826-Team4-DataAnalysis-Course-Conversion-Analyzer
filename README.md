Sem 5 Sprint 1 S67 Team 4

# Course Conversion Analyzer

## Problem
An online learning platform receives many course views and preview interactions, but some highly viewed courses still receive relatively few enrollments. The goal is to understand what factors may be associated with this poor conversion.

## Objective
The objective of this project is to identify highly viewed courses with low enrollment conversion and analyse whether factors such as price, rating, preview engagement, and category are associated with their performance.

## Dataset
The dataset contains 8 online courses with information about:

- Course name
- Category
- Price
- Rating
- Views
- Preview clicks
- Enrollments

The data is cleaned with Pandas, analysed with conversion metrics, and stored in SQLite for SQL-based analysis.

## Technologies

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Plotly
- Streamlit

## How the Analysis Works

1. Load and inspect the raw course data.
2. Clean missing, duplicate, invalid, and inconsistent values.
3. Calculate conversion rate and preview-to-enrollment conversion.
4. Identify courses with above-average views and below-average conversion.
5. Compare these courses based on price, rating, preview engagement, and category.
6. Store the data in SQLite and reproduce key analyses using SQL.
7. Present the results through an interactive Streamlit dashboard.

## Dashboard

### Main Dashboard

![Course Conversion Dashboard](screenshots/dashboard.png)

### Conversion Analysis

![Conversion Analysis](screenshots/analysis.png)

## Main Findings

- High-view, low-conversion courses have a much lower average conversion rate than the other courses in the dataset.
- The problematic courses also have a higher average price and a lower average rating.
- Preview-to-enrollment conversion is substantially lower for the problematic courses than for the other courses.
- Programming and Data Science contain the flagged courses in this dataset.

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline

```bash
python src/inspect_data.py
python src/clean_data.py
python src/calculate_metrics.py
python src/analysis.py
python src/create_database.py
streamlit run app.py
```

### 3. Open the dashboard

Streamlit will provide a local URL, usually `http://localhost:8501`.

## Project Structure

```text
course-conversion-analyzer/
├── data/
│   ├── courses.csv
│   ├── cleaned_courses.csv
│   ├── analyzed_courses.csv
│   └── courses.db
├── screenshots/
│   ├── dashboard.png
│   └── analysis.png
├── sql/
│   └── analysis.sql
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── calculate_metrics.py
│   ├── analysis.py
│   ├── create_database.py
│   ├── analyze_data.py
│   └── store_to_sql.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```









cd /Users/vaibhaavbs/Downloads/CodingProjects/Sem5_Sprint1/course-conversion-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/inspect_data.py
python src/clean_data.py
python src/calculate_metrics.py
python src/analysis.py
python src/create_database.py

# Launch the dashboard
streamlit run app.py