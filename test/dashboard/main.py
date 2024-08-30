from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

import awswrangler as wr
import boto3

import plotly.graph_objs as go
import datetime


# Page config
st.set_page_config(layout="wide")

# Set title
st.title("LiteDQ Overview")

@st.cache_data
def load_data():
    # Get data from AWS
    session = boto3.Session()
    data_pd = wr.athena.read_sql_query(
        "SELECT * FROM logs", 
        database="datalogger", 
        boto3_session=session
    )

    # Make overview
    overview_pd = (
        data_pd.assign(exec_dt=lambda x: pd.to_datetime(x.exec_dt).dt.date)
        .groupby("exec_dt")
        .agg(passed=("result", "sum"), total=("result", "count"))
        .assign(passed_pct=lambda x: round(x.passed / x.total, 2))
        .assign(failed=lambda x: x.total - x.passed)
        .assign(color=lambda x: np.where(x.passed_pct > 0.5, "#00A170", "#F08080"))
        .reset_index()
    )

    # Get distinct qids and their pass rate
    qid_rate_pd = (data_pd
        .assign(exec_dt=lambda x: pd.to_datetime(x.exec_dt).dt.date)
        .groupby(["question_id", "exec_dt"])
        .agg(passed=("result", "sum"), total=("result", "count"))
        .assign(passed_pct=lambda x: round(x.passed / x.total, 3))
        .assign(failed=lambda x: x.total - x.passed)
        .assign(color=lambda x: np.where(x.passed_pct > 0.5, "#00A170", "#F08080"))
        .reset_index()
    )

    return overview_pd, qid_rate_pd, data_pd


overview_pd, qid_rate_pd, data_pd = load_data()


def plot_exec_pass_rate(overview_pd):
    # Make plot
    fig_overview = go.Figure(
        [
            go.Scatter(
                x=overview_pd.exec_dt,
                y=overview_pd.passed_pct,
                mode="lines+markers",
                marker=dict(size=10, color=overview_pd.color),
                hovertemplate="<br><b>Date</b>: %{x}<br>"
                + "<b>Successful Checks</b>: %{y}"
                + "<extra></extra>",
            )
        ]
    )

    # Update layout and other params
    fig_overview.update_layout(
        yaxis_tickformat=".1%",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=20, b=10),
    )

    fig_overview.update_traces(line_color="#4099da")

    return fig_overview

def plot_groups_pass_rate(data_pd):
    # Create groups data
    groups_pd = (
        data_pd.filter(items=["question_id", "result"])
        .groupby("question_id")
        .value_counts()
        .to_frame()
        .reset_index()
        .pivot(index="question_id", columns="result", values="count")
        .reset_index()
        .rename(columns={False: "Failed", True: "Passed"})
        .sort_values(by="Failed", ascending=False)
    )

    # Make plot
    fig_groups = go.Figure(
        [
            go.Bar(
                name="Passed",
                y=groups_pd["question_id"],
                x=groups_pd["Passed"],
                orientation="h",
                marker=dict(color="#00A170"),
                hovertemplate="<b>Checks Passed </b>: %{x}<extra></extra>",
            ),
            go.Bar(
                name="Failed",
                y=groups_pd["question_id"],
                x=groups_pd["Failed"],
                orientation="h",
                marker=dict(color="#F08080"),
                hovertemplate="<b>Checks Failed </b>: %{x}<extra></extra>",
            ),
        ]
    )

    fig_groups.update_traces(width=0.2)

    # Update layout
    fig_groups.update_layout(
        margin_pad=10,
        showlegend=False,
        height=200,
        barmode="stack",
        bargap=0,
        bargroupgap=0,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )

    # Update axes
    fig_groups.update_yaxes(tickfont=dict(size=12))

    return fig_groups




overview_fig  = plot_exec_pass_rate(overview_pd)
pass_rate_fig = plot_groups_pass_rate(data_pd)

def md_card(title, x, color=""):
    return f"""
        <p style="text-align:center; font-size:20px; font-weight: bolder;">{title}</p>
        <p style="text-align:center; font-size:40px; color: {color}">{x}</p>
    """


with st.container(border=True):
    st.subheader("Daily Executions Pass Rate", divider="red")
    st.plotly_chart(overview_fig)

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True, height=316):
        st.subheader("Questions Pass Rate", divider="red")
        st.plotly_chart(pass_rate_fig)


with col2:
    left, right = st.columns(2)
    avg_pass_rate = 100.0 * (overview_pd.passed / overview_pd.total).mean()
    delta = (datetime.date.today() - overview_pd.exec_dt.max()).days
    last_exec_dt = overview_pd.exec_dt.max()

    n_apps = data_pd.query("exec_dt == exec_dt.max()").exec_id.nunique()
    n_ques = data_pd.query("exec_dt == exec_dt.max()").question_id.nunique()
    
    with left:
        st.container(border=True, height=150).markdown(
            md_card("Avg. Pass Rate", f"{avg_pass_rate:0.2f}%", "#F08080" if avg_pass_rate < 50 else "#00A170"), 
            unsafe_allow_html=True
        )
        st.container(border=True, height=150).markdown(
            md_card("# Applications", n_apps),
            unsafe_allow_html=True
        )

    with right:
        st.container(border=True, height=150).markdown(
            md_card("Last Execution", f"{last_exec_dt}", "#F08080" if delta >= 7 else "#00A170"),
            unsafe_allow_html=True
        )

        st.container(border=True, height=150).markdown(
            md_card("# Questions", n_ques),
            unsafe_allow_html=True
        )


