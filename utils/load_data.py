import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/gold_data_fe.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df