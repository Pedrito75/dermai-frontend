import pandas as pd
import altair as alt
import streamlit as st

def results_chart(pred: pd.DataFrame):
    chart = (
        alt.Chart(pred)
        .mark_bar()
        .encode(
            y=alt.Y("index:N", title="Classes", sort="-x"),
            x=alt.X("Probabilities:Q"),
            color=alt.Color("hexa:N", scale=None),
            tooltip=["Probabilities"],
        )
    )
    st.altair_chart(chart, width="stretch")
