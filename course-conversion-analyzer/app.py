import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from typing import Union


# ---------- Page config ----------
st.set_page_config(
    page_title="Course Conversion Analyzer",
    page_icon="📊",
    layout="wide",
)


# ---------- Theme state & color setup ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

is_dark = st.session_state.theme == "dark"
PLOTLY_TEMPLATE = "plotly_dark" if is_dark else "plotly_white"
TEXT_COLOR = "#F0F6FC" if is_dark else "#1E293B"
SECONDARY_TEXT_COLOR = "#8B949E" if is_dark else "#475569"
GRID_COLOR = "rgba(255, 255, 255, 0.06)" if is_dark else "rgba(30, 41, 59, 0.06)"
OTHER_COLOR = "#6C8CFF" if is_dark else "#2563EB"
MEDIAN_LINE_COLOR = "#8B949E" if is_dark else "#64748B"
HOVER_BG = "#161B22" if is_dark else "#FFFFFF"
HOVER_BORDER = "#30363D" if is_dark else "#E2E8F0"


def themed_dataframe(data: Union[pd.DataFrame, pd.Series], **kwargs):
    """Render a dataframe/series with theme-aware styling, formatted numbers,
    framed card borders, and soft red/coral highlighting for flagged courses."""
    if isinstance(data, pd.Series):
        series_name = data.name or "Course Count"
        index_name = data.index.name or "category"
        df_to_show = data.reset_index()
        df_to_show.columns = [index_name, series_name]
    else:
        df_to_show = data.copy()

    has_flag_col = "high_view_low_conversion" in df_to_show.columns
    flag_series = df_to_show["high_view_low_conversion"] if has_flag_col else None
    
    # Exclude helper flag column from visible columns
    display_df = df_to_show.drop(columns=["high_view_low_conversion"]) if has_flag_col else df_to_show

    format_dict = {}
    if "conversion_rate" in display_df.columns:
        format_dict["conversion_rate"] = "{:.2%}"
    if "preview_conversion" in display_df.columns:
        format_dict["preview_conversion"] = "{:.2%}"
    if "price" in display_df.columns:
        format_dict["price"] = "₹{:,.0f}"
    if "views" in display_df.columns:
        format_dict["views"] = "{:,}"
    if "preview_clicks" in display_df.columns:
        format_dict["preview_clicks"] = "{:,}"
    if "enrollments" in display_df.columns:
        format_dict["enrollments"] = "{:,}"
    if "rating" in display_df.columns:
        format_dict["rating"] = "{:.2f}"

    bg_color = "#161B22" if is_dark else "#FFFFFF"
    text_color = "#F0F6FC" if is_dark else "#1E293B"
    header_bg = "#1F242D" if is_dark else "#F8FAFC"
    header_text_color = "#8B949E" if is_dark else "#475569"
    border_color = "#30363D" if is_dark else "#E2E8F0"
    outer_border_color = "#30363D" if is_dark else "#CBD5E1"

    flagged_row_bg = "rgba(255, 107, 74, 0.12)" if is_dark else "#FFF2EF"
    flagged_text_accent = "#FF6B4A" if is_dark else "#E0533C"

    styler = display_df.style
    if format_dict:
        styler = styler.format(format_dict)

    styler = styler.set_properties(
        **{
            "background-color": bg_color,
            "color": text_color,
            "border-color": border_color,
        }
    )

    if flag_series is not None:
        def style_rows(df_slice):
            styles = pd.DataFrame("", index=df_slice.index, columns=df_slice.columns)
            for idx in df_slice.index:
                if flag_series.get(idx, False):
                    styles.loc[idx, :] = f"background-color: {flagged_row_bg};"
                    if "conversion_rate" in styles.columns:
                        styles.loc[idx, "conversion_rate"] = (
                            f"background-color: {flagged_row_bg}; color: {flagged_text_accent}; font-weight: 700;"
                        )
                    if "preview_conversion" in styles.columns:
                        styles.loc[idx, "preview_conversion"] = (
                            f"background-color: {flagged_row_bg}; color: {flagged_text_accent}; font-weight: 700;"
                        )
            return styles

        styler = styler.apply(style_rows, axis=None)

    styler = styler.set_table_styles([
        {
            "selector": "th, th.col_heading, th.row_heading, th.blank, th.index_name",
            "props": [
                ("background-color", f"{header_bg} !important"),
                ("color", f"{header_text_color} !important"),
                ("font-weight", "700 !important"),
                ("border-bottom", f"1px solid {outer_border_color} !important"),
                ("border-right", f"1px solid {border_color} !important"),
                ("padding", "10px 14px !important"),
            ],
        },
        {
            "selector": "td, td.row_heading",
            "props": [
                ("border-bottom", f"1px solid {border_color} !important"),
                ("border-right", f"1px solid {border_color} !important"),
                ("padding", "10px 14px !important"),
            ],
        },
        {
            "selector": "table",
            "props": [
                ("border", f"1px solid {outer_border_color} !important"),
                ("border-radius", "10px !important"),
                ("border-collapse", "separate !important"),
                ("border-spacing", "0 !important"),
                ("width", "100% !important"),
            ],
        }
    ])
    st.dataframe(styler, **kwargs)


# ---------- Load CSS & Theme JavaScript ----------
def load_css(path: Path) -> str:
    with open(path) as file:
        return file.read()


base_dir = Path(__file__).resolve().parent
css_path = base_dir / "assets" / "styles.css"
st.markdown(f"<style>{load_css(css_path)}</style>", unsafe_allow_html=True)

# Sentinel div + JS snippet to sync document-level theme attributes
st.markdown(
    f'''
    <div class="theme-sentinel" data-theme="{st.session_state.theme}" style="display:none;"></div>
    <script>
        (function() {{
            const theme = "{st.session_state.theme}";
            document.documentElement.setAttribute('data-theme', theme);
            const stApp = document.querySelector('.stApp');
            if (stApp) stApp.setAttribute('data-theme', theme);
        }})();
    </script>
    ''',
    unsafe_allow_html=True,
)


# ---------- Data ----------
@st.cache_data
def load_data():
    data_path = base_dir / "data" / "analyzed_courses.csv"
    return pd.read_csv(data_path)


df = load_data()


# ---------- Header row: title + theme toggle ----------
title_col, toggle_col = st.columns([6, 1])

with title_col:
    st.title("Course Conversion Analyzer")
    st.write(
        "Analyze course views, previews, and enrollments to identify why highly viewed courses fail to convert."
    )

with toggle_col:
    label = "🌙 Dark" if is_dark else "☀️ Light"
    if st.button(label, use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()


# ---------- Glossary ----------
with st.expander("📖 What do these terms mean?"):
    st.markdown(
        """
        - <span class="glossary-term">Conversion rate</span> — `enrollments ÷ views`. The share of everyone who viewed a course who went on to enroll. This is the headline metric for how well a course turns interest into signups.
        - <span class="glossary-term">Preview conversion</span> — `enrollments ÷ preview clicks`. Of the people who clicked to preview the course (a stronger interest signal than a view), what share actually enrolled. A low preview conversion is a stronger warning sign than a low overall conversion rate, since these are people who were already fairly interested.
        - <span class="glossary-term">High Views / Low Conversion</span> — a course whose views are at or above the dataset's median, and whose conversion rate is at or below the median. These are the courses this project is built to explain.
        - <span class="glossary-term">Median thresholds (dashed lines)</span> — the midpoint value across all courses in the current selection, used as the cutoff for "high" and "low" instead of an arbitrary fixed number.
        """,
        unsafe_allow_html=True,
    )

st.divider()


# ---------- Filters ----------
categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.selectbox("Category", categories)

min_price = float(df["price"].min())
max_price = float(df["price"].max())
price_range = st.slider(
    "Price range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

filtered_df = filtered_df[
    (filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])
]

filtered_df = filtered_df.copy()
filtered_df["performance"] = filtered_df["high_view_low_conversion"].map(
    {True: "High Views / Low Conversion", False: "Other"}
)

st.divider()


# ---------- KPI cards + gauge ----------
def kpi_card(label: str, value: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if len(filtered_df) > 0:
    total_views = filtered_df["views"].sum()
    total_enrollments = filtered_df["enrollments"].sum()
    average_conversion = filtered_df["conversion_rate"].mean()
    problem_count = int(filtered_df["high_view_low_conversion"].sum())

    col1, col2, col3 = st.columns([1, 1, 1.4])

    with col1:
        kpi_card("Total Views", f"{total_views:,}", f"{len(filtered_df)} courses in view")

    with col2:
        kpi_card("Enrollments", f"{total_enrollments:,}", f"{problem_count} flagged as underperforming")

    with col3:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=average_conversion * 100,
                number={"suffix": "%", "font": {"size": 34, "color": TEXT_COLOR}},
                title={"text": "Avg Conversion Rate", "font": {"size": 14, "color": TEXT_COLOR}},
                gauge={
                    "axis": {
                        "range": [0, max(15, average_conversion * 100 * 1.5)],
                        "tickcolor": SECONDARY_TEXT_COLOR,
                        "tickfont": {"size": 11, "color": SECONDARY_TEXT_COLOR},
                    },
                    "bar": {"color": "#FF6B4A"},
                    "steps": [
                        {"range": [0, 3], "color": "rgba(248,113,113,0.35)" if is_dark else "rgba(239,68,68,0.18)"},
                        {"range": [3, 8], "color": "rgba(250,204,21,0.30)" if is_dark else "rgba(234,179,8,0.18)"},
                        {"range": [8, 20], "color": "rgba(74,222,128,0.30)" if is_dark else "rgba(34,197,94,0.18)"},
                    ],
                },
            )
        )
        gauge.update_layout(
            template=PLOTLY_TEMPLATE,
            height=160,
            margin=dict(l=20, r=20, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_COLOR),
        )
        st.plotly_chart(gauge, use_container_width=True)
else:
    st.info("No courses match the selected filters.")

st.divider()


# ---------- Scatter plot ----------
high_view_threshold = df["views"].median()
low_conversion_threshold = df["conversion_rate"].median()

st.markdown(
    '<div class="section-header"><span class="icon">📈</span><h3>Views vs Conversion Rate</h3></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="chart-caption">
    Each point is one course. The X-axis is how many times it was viewed; the Y-axis is what
    share of those viewers enrolled. The dashed lines mark the median views and median conversion
    rate across all courses. Points in the lower-right — high views, low conversion — are colored
    orange: they attract plenty of traffic but convert it poorly.
    </div>
    """,
    unsafe_allow_html=True,
)

fig = px.scatter(
    filtered_df,
    x="views",
    y="conversion_rate",
    color="performance",
    color_discrete_map={
        "High Views / Low Conversion": "#FF6B4A",
        "Other": OTHER_COLOR,
    },
    hover_name="course_name",
    hover_data=["category", "price", "rating", "preview_clicks", "enrollments"],
    labels={
        "views": "Views",
        "conversion_rate": "Conversion Rate",
        "performance": "Performance",
    },
)
fig.add_vline(
    x=high_view_threshold,
    line_dash="dash",
    line_color=MEDIAN_LINE_COLOR,
    annotation_text="median views",
    annotation_position="top right",
    annotation_font_color=SECONDARY_TEXT_COLOR,
    annotation_font_size=12,
)
fig.add_hline(
    y=low_conversion_threshold,
    line_dash="dash",
    line_color=MEDIAN_LINE_COLOR,
    annotation_text="median conversion",
    annotation_position="bottom right",
    annotation_font_color=SECONDARY_TEXT_COLOR,
    annotation_font_size=12,
)
fig.update_layout(
    template=PLOTLY_TEMPLATE,
    yaxis_tickformat=".0%",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_COLOR),
    xaxis=dict(
        gridcolor=GRID_COLOR,
        title=dict(font=dict(color=TEXT_COLOR, size=13)),
        tickfont=dict(color=SECONDARY_TEXT_COLOR, size=12),
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR,
        title=dict(font=dict(color=TEXT_COLOR, size=13)),
        tickfont=dict(color=SECONDARY_TEXT_COLOR, size=12),
    ),
    legend=dict(
        font=dict(color=TEXT_COLOR, size=12),
        title=dict(font=dict(color=TEXT_COLOR, size=12)),
    ),
    hoverlabel=dict(
        bgcolor=HOVER_BG,
        font_size=13,
        font_color=TEXT_COLOR,
        bordercolor=HOVER_BORDER,
    ),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()


# ---------- Problem courses table ----------
st.markdown(
    '<div class="section-header"><span class="icon">🔍</span><h3>High-View / Low-Conversion Courses</h3></div>',
    unsafe_allow_html=True,
)
problem_courses = filtered_df[filtered_df["high_view_low_conversion"]]

if len(problem_courses) > 0:
    problem_table = problem_courses[
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
    themed_dataframe(problem_table, use_container_width=True, hide_index=True)

    st.divider()

    st.markdown(
        '<div class="section-header"><span class="icon">🧭</span><h3>Why Are They Underperforming?</h3></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="chart-caption">Comparing the flagged courses against every other course in the current selection.</div>',
        unsafe_allow_html=True,
    )

    other_courses = filtered_df[~filtered_df["high_view_low_conversion"]]

    if len(other_courses) > 0:
        problem_price = problem_courses["price"].mean()
        other_price = other_courses["price"].mean()
        problem_rating = problem_courses["rating"].mean()
        other_rating = other_courses["rating"].mean()
        problem_preview = problem_courses["preview_conversion"].mean()
        other_preview = other_courses["preview_conversion"].mean()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Price",
                f"₹{problem_price:,.0f}",
                f"vs ₹{other_price:,.0f}",
                delta_color="inverse",
                help="Higher price for the flagged courses vs. the rest — shown in red because it's the unfavorable direction.",
            )
        with col2:
            st.metric(
                "Average Rating",
                f"{problem_rating:.2f}",
                f"vs {other_rating:.2f}",
                delta_color="inverse",
                help="Rating of the flagged courses vs. the rest.",
            )
        with col3:
            st.metric(
                "Preview Conversion",
                f"{problem_preview * 100:.2f}%",
                f"vs {other_preview * 100:.2f}%",
                delta_color="inverse",
                help="Of people who clicked preview, the share who enrolled — flagged courses vs. others.",
            )

        st.write("Categories containing problematic courses:")
        themed_dataframe(
            problem_courses["category"].value_counts().rename("Course Count"),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No comparison group remains after applying the selected filters.")
else:
    st.info("No high-view, low-conversion courses match the selected filters.")

st.divider()


# ---------- Key findings ----------
st.markdown(
    '<div class="section-header"><span class="icon">💡</span><h3>Key Findings</h3></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    - High-view, low-conversion courses have a much lower average conversion rate than the other courses in the dataset.
    - The problematic courses also have a higher average price and a lower average rating.
    - Preview-to-enrollment conversion is substantially lower for the problematic courses than for the other courses.
    - Programming and Data Science contain the flagged courses in this dataset.
    """
)

st.divider()


# ---------- Full table ----------
st.markdown(
    '<div class="section-header"><span class="icon">📋</span><h3>Course Performance</h3></div>',
    unsafe_allow_html=True,
)
themed_dataframe(
    filtered_df[
        [
            "course_name",
            "category",
            "price",
            "rating",
            "views",
            "preview_clicks",
            "enrollments",
            "conversion_rate",
            "high_view_low_conversion",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)