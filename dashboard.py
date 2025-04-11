
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("fast_lesson_completions.csv")
df["current_lesson_datetime"] = pd.to_datetime(df["current_lesson_datetime"])
df["next_lesson_datetime"] = pd.to_datetime(df["next_lesson_datetime"])
df["date"] = pd.to_datetime(df["current_lesson_datetime"]).dt.date

st.set_page_config(page_title="Fast Lesson Completions", layout="wide")

st.title("📊 Lessons Completed in Under 5 Seconds")
st.markdown("**Cohort: Data Analyst – April 2020**")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Suspicious Completions", len(df))
col2.metric("Unique Lessons", df["lesson_id"].nunique())
col3.metric("Unique Users", df["user_id"].nunique())

st.markdown("---")

# Bar chart: Frequency per lesson
lesson_freq = df.groupby("lesson_name").size().reset_index(name="count").sort_values("count", ascending=False)
fig_bar = px.bar(lesson_freq, x="count", y="lesson_name", orientation="h", title="Frequency of Fast Completions per Lesson")
st.plotly_chart(fig_bar, use_container_width=True)

# Histogram of delta_seconds
fig_hist = px.histogram(df, x="delta_seconds", nbins=10, title="Distribution of Delta Seconds")
st.plotly_chart(fig_hist, use_container_width=True)

# Timeline
timeline = df.groupby("date").size().reset_index(name="count")
fig_time = px.line(timeline, x="date", y="count", markers=True, title="Suspicious Events Over Time")
st.plotly_chart(fig_time, use_container_width=True)

# Detailed table
st.subheader("📋 Affected Lessons")
st.dataframe(df[["lesson_id", "lesson_name", "user_id", "delta_seconds", "date"]].sort_values("lesson_id"))
