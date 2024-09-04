from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

import awswrangler as wr
import boto3

import plotly.graph_objs as go
import datetime

from sections.overview import show_overview
from sections.details import show_details


# Page config
st.set_page_config(layout="wide", page_title="LiteDQ Dashboard")

if "page" not in st.session_state:
    st.session_state.page = "overview"

if "search_text" not in st.session_state:
    st.session_state.search_text = ""



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
        .assign(passed_pct=lambda x: round(x.passed / x.total, 3))
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


# Force reload if we have new data
overview_pd, qid_rate_pd, data_pd = load_data()


def switch_page(page):
    st.session_state.page = page

with st.sidebar:
    with st.container():
        st.header("Pages")
        st.button(
            "Overview", 
            on_click=switch_page, 
            args=["overview"], 
            use_container_width=True, 
            type="primary" if st.session_state.page == "overview" else "secondary"
        )
        st.button(
            "Details", 
            on_click=switch_page, 
            args=["details"], 
            use_container_width=True,
            type="primary" if st.session_state.page == "details" else "secondary"
        )

    with st.container():
        st.header("Options")
        if st.button("Reload Data", use_container_width=True):
            load_data.clear()
            st.rerun()



if st.session_state.page == "overview":        
    show_overview(data_pd, overview_pd)

elif st.session_state.page == "details":        
    show_details(data_pd, qid_rate_pd)
