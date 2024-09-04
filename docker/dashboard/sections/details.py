from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

import awswrangler as wr
import boto3

import plotly.graph_objs as go
import datetime
import json
from fuzzywuzzy import process 


def plot_qid_pass_rate(qid, qid_rate_pd):
    rate_pd = qid_rate_pd.query(f"question_id == '{qid}'")

    fig = go.Figure(
        [
            go.Scatter(
                x=rate_pd.exec_dt,
                y=rate_pd.passed_pct,
                mode="lines+markers",
                marker=dict(size=10, color=rate_pd.color),
                hovertemplate="<br><b>Date</b>: %{x}<br>"
                + "<b>Successful Checks</b>: %{y}"
                + "<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        yaxis_tickformat=".1%",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=10, r=10, t=20, b=10),
        height=200,
    )
    fig.update_traces(line_color="#4099da")

    return fig

def make_qid_card(qid, data_pd, qid_rate_pd):
    # Get latest entry
    exec_pd = data_pd.query(f"question_id == '{qid}' and exec_dt == exec_dt.max()")

    # Get attributes
    desc = exec_pd.question_desc.iloc[0]
    stat = exec_pd.result.iloc[0]
    last_date = exec_pd.exec_dt.iloc[0]

    subject = json.loads(exec_pd.subject.iloc[0].replace("'", "\"") or "{}")
    subject_pd = pd.DataFrame.from_records(
        [subject] if isinstance(subject, dict) else subject

    )

    # Get pass rate
    fig_pass_rate = plot_qid_pass_rate(qid, qid_rate_pd)

    with st.expander(qid.upper()):
        if stat:
            st.success(f"Last execution **SUCCEEDED** on {last_date.date()}")
        else:
            st.error(f"Last execution **FAILED** on {last_date.date()}")

        st.subheader("Description")
        st.markdown(desc)
        
        if not subject_pd.empty:
            st.subheader("Subject")
            st.dataframe(subject_pd, use_container_width=True, hide_index=True, )
        
        st.subheader("Daily Pass Rate")
        st.plotly_chart(fig_pass_rate)


def search_callback():
    st.session_state.qid_search = ""
    

def show_details(data_pd, qid_rate_pd):
    # Prepare data
    passed_qids = (data_pd
        .query(f"result == True and exec_dt == exec_dt.max()")
        .question_id
        .unique()
    )

    failed_qids = (data_pd
        .query(f"result == False and exec_dt == exec_dt.max()")
        .question_id
        .unique()
    )
    
    st.title("Details")

    c1, c2 = st.columns([1, 0.1], vertical_alignment="bottom", )
    with c1:
        search_input = st.text_input(
            placeholder="Question ID", 
            label="Search for a specific question ID", 
            key="qid_search",
        )

    with c2:
        st.empty()
        st.button("Clear", on_click=search_callback, use_container_width=True)
    
    passed_matches = passed_qids
    failed_matches = failed_qids

    if search_input:
        passed_matches = [x[0] for x in process.extract(search_input, choices=passed_qids) if x[1] > 50]
        failed_matches = [x[0] for x in process.extract(search_input, choices=failed_qids) if x[1] > 50]


    st.markdown("## :green[Passed Checks]")
    for qid in passed_matches:
        make_qid_card(qid, data_pd, qid_rate_pd)

    
    
    st.markdown("## :red[Failed Checks]")
    for qid in failed_matches:
        make_qid_card(qid, data_pd, qid_rate_pd)


