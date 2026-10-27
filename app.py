import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# Custom Styling
# -------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .main-title {
        font-size: 32px;
        font-weight: 750;
        margin-bottom: 2px;
    }
    .subtitle {
        color: #8b95a5;
        font-size: 15px;
        margin-bottom: 24px;
    }
    div[data-testid="stMetric"] {
        background: #172235;
        border: 1px solid #29374d;
        padding: 18px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Student Dataset
# -------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "student_data.csv"
    data = pd.read_csv(file_path)

    required_columns = [
        "Student", "Department", "Attendance",
        "Assignment", "MST", "Final Exam"
    ]

    missing_columns = [
        col for col in required_columns if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing_columns)
        )

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load student_data.csv: {error}")
    st.stop()

# -------------------------------
# Data Processing
# -------------------------------
df["Total"] = df["Assignment"] + df["MST"] + df["Final Exam"]
df["Percentage"] = (df["Total"] / 120) * 100


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


df["Grade"] = df["Percentage"].apply(calculate_grade)

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("🎓 Student Analytics")
st.sidebar.caption("Performance monitoring system")
st.sidebar.divider()

departments = sorted(df["Department"].dropna().unique().tolist())

selected_departments = st.sidebar.multiselect(
    "Select Department",
    options=departments,
    default=departments
)

grade_options = ["A+", "A", "B", "C", "D", "F"]

selected_grades = st.sidebar.multiselect(
    "Select Grade",
    options=grade_options,
    default=grade_options
)

search = st.sidebar.text_input("🔎 Search student")

filtered_df = df[
    df["Department"].isin(selected_departments)
    & df["Grade"].isin(selected_grades)
]

if search.strip():
    filtered_df = filtered_df[
        filtered_df["Student"].astype(str).str.contains(
            search.strip(), case=False, na=False
        )
    ]

st.sidebar.divider()
st.sidebar.caption("Student Performance Analysis System")
st.sidebar.caption("Built with Python · Pandas · Plotly")

# -------------------------------
# Dashboard Header
# -------------------------------
st.markdown(
    '<div class="main-title">Student Performance Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">'
    'Academic insights, grade analysis and attendance monitoring'
    '</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No students match the selected filters.")
    st.stop()

# -------------------------------
# Summary Cards
# -------------------------------
total_students = len(filtered_df)
average_percentage = filtered_df["Percentage"].mean()
highest_percentage = filtered_df["Percentage"].max()
low_attendance_count = (filtered_df["Attendance"] < 75).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Students", total_students)
c2.metric("📊 Average Percentage", f"{average_percentage:.2f}%")
c3.metric("🏆 Highest Percentage", f"{highest_percentage:.2f}%")
c4.metric("⚠️ Low Attendance", int(low_attendance_count))

st.divider()

# -------------------------------
# Performance Charts
# -------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Department-wise Performance")

    department_average = (
        filtered_df.groupby("Department", as_index=False)["Percentage"]
        .mean()
    )

    fig_department = px.bar(
        department_average,
        x="Department",
        y="Percentage",
        color="Department",
        text=department_average["Percentage"].round(2),
        title="Average Percentage by Department",
        template="plotly_dark"
    )

    fig_department.update_layout(
        showlegend=False,
        yaxis_title="Average Percentage",
        xaxis_title="Department"
    )
    st.plotly_chart(fig_department, use_container_width=True)

with right:
    st.subheader("Grade Distribution")

    grade_counts = (
        filtered_df["Grade"]
        .value_counts()
        .reindex(grade_options, fill_value=0)
        .reset_index()
    )
    grade_counts.columns = ["Grade", "Students"]
    grade_counts = grade_counts[grade_counts["Students"] > 0]

    fig_grade = px.pie(
        grade_counts,
        names="Grade",
        values="Students",
        hole=0.48,
        title="Distribution of Student Grades",
        template="plotly_dark"
    )

    fig_grade.update_traces(
        textposition="inside",
        textinfo="label+percent"
    )
    st.plotly_chart(fig_grade, use_container_width=True)

# -------------------------------
# Student Percentage Chart
# -------------------------------
st.subheader("Individual Student Performance")

chart_df = filtered_df.sort_values("Percentage", ascending=False)

fig_students = px.bar(
    chart_df,
    x="Student",
    y="Percentage",
    color="Grade",
    hover_data=["Department", "Total", "Attendance"],
    title="Student Percentage Comparison",
    template="plotly_dark"
)

fig_students.update_layout(
    xaxis_title="Student",
    yaxis_title="Percentage",
    xaxis_tickangle=-45
)

st.plotly_chart(fig_students, use_container_width=True)

st.divider()

# -------------------------------
# Top 5 Students
# -------------------------------
st.subheader("🏆 Top Performing Students")

top_students = filtered_df.nlargest(5, "Percentage")

st.dataframe(
    top_students[
        ["Student", "Department", "Total", "Percentage", "Grade"]
    ].round(2),
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# Attendance Monitoring
# -------------------------------
st.subheader("⚠️ Attendance Monitoring")
st.caption("Students with attendance below 75%")

low_attendance = filtered_df[
    filtered_df["Attendance"] < 75
].sort_values("Attendance")

if low_attendance.empty:
    st.success("No students below 75% attendance in this selection.")
else:
    st.dataframe(
        low_attendance[
            ["Student", "Department", "Attendance"]
        ],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------
# Complete Student Records
# -------------------------------
st.divider()
st.subheader("📋 Complete Student Records")

st.dataframe(
    filtered_df[
        [
            "Student", "Department", "Attendance",
            "Assignment", "MST", "Final Exam",
            "Total", "Percentage", "Grade"
        ]
    ].sort_values("Percentage", ascending=False).round(2),
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# Download Filtered Results
# -------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Student Report (CSV)",
    data=csv_data,
    file_name="student_performance_report.csv",
    mime="text/csv"
)

st.caption("Student Performance Analysis System · Python Data Analytics")