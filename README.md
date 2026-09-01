Sem 5 Sprint 1 S67 Team 4

# Course Conversion Analyzer

## Problem

An online learning platform receives many course views and preview interactions, but some highly viewed courses still receive relatively few enrollments. This project investigates what factors may be associated with poor course conversion.

## Objective

The objective is to identify highly viewed courses with low enrollment conversion and analyse whether factors such as price, rating, preview engagement, and category are associated with their performance.

## Dataset

The dataset contains 8 online courses with the following information:

* Course name
* Category
* Price
* Rating
* Views
* Preview clicks
* Enrollments

The data is cleaned using Pandas, analysed using conversion metrics, and stored in SQLite for SQL-based analysis.

## Technologies

* Python
* Pandas
* NumPy
* SQLite
* SQL
* Plotly
* Streamlit

## Analysis Workflow

1. Load and inspect the raw course data.
2. Clean missing, duplicate, invalid, and inconsistent values.
3. Calculate enrollment conversion rate and preview-to-enrollment conversion.
4. Identify courses with at least median views and at most median conversion.
5. Compare flagged courses with the remaining courses using price, rating, views, preview engagement, and conversion metrics.
6. Store the processed data in SQLite and reproduce key analyses using SQL.
7. Present the results through an interactive Streamlit dashboard.

## Main Findings

* High-view, low-conversion courses have a substantially lower average conversion rate than the other courses: approximately **0.0164 vs 0.0722**.
* The flagged courses have a higher average price: approximately **2749 vs 1682.33**.
* The flagged courses have a lower average rating: approximately **3.80 vs 4.1833**.
* Preview-to-enrollment conversion is substantially lower for the flagged courses: approximately **0.0534 vs 0.1543**.
* **Programming** and **Data Science** contain the flagged courses in this dataset.

These findings represent associations observed in a very small dataset and should not be interpreted as evidence of causation.

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python src/inspect_data.py
python src/clean_data.py
python src/calculate_metrics.py
python src/analysis.py
python src/create_database.py
```

### 3. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

`http://localhost:8501`

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
