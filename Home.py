import streamlit as st

st.set_page_config(
    page_title="Gold Price Dashboard",
    page_icon="📈",
    layout="wide"
)

# HERO SECTION
col1, col2 = st.columns([2,1])

with col1:
    st.title("📈 Gold Price Analysis Dashboard")

    st.markdown("""
    ### Forecasting Gold Price Using Time Series Analysis

    Dashboard ini menyajikan analisis harga emas historis,
    hasil feature engineering, serta insight yang digunakan
    untuk pengembangan model LSTM dan GRU.
    """)

    st.markdown("")

    st.markdown("""
    ### 🎯 Project Objectives

    - Menganalisis tren harga emas historis
    - Mengevaluasi volatilitas dan momentum pasar
    - Mengeksplorasi hubungan antar fitur
    - Menyiapkan dataset untuk model LSTM & GRU
    """)

with col2:
    st.image(
        "assets/gold_banner.jpg",
        width="stretch"
    )

# PROJECT INFORMATION
st.divider()

st.subheader("📌 Project Information")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📊 Data Source")
        st.write("##### Yahoo Finance")
        st.caption("Historical daily gold price data")

with col2:
    with st.container(border=True):
        st.markdown("### 🤖 Forecasting Models")
        st.write("##### LSTM & GRU")
        st.caption(
            "Deep learning models for time series forecasting"
        )

with col3:
    with st.container(border=True):
        st.markdown("### ⚙️ Engineered Features")
        st.write(
            "##### Lag, EMA, Momentum, Volatility, High Low Spread"
        )
        st.caption(
            "Features created to capture trends and volatility"
        )

# DASHBOARD NAVIGATION
st.divider()

st.subheader("🧭 Dashboard Navigation")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.markdown("### 📊 Overview")

        st.write(
            "Menampilkan ringkasan dataset, statistik utama, "
            "dan tren harga emas historis."
        )

    with st.container(border=True):
        st.markdown("### 📈 Price Analysis")

        st.write(
            "Menganalisis pergerakan harga Open, High, Low, "
            "dan Close melalui berbagai visualisasi."
        )

with col2:

    with st.container(border=True):
        st.markdown("### ⚙️ Feature Engineering")

        st.write(
            "Menampilkan fitur hasil rekayasa data seperti "
            "EMA, Lag Features, Momentum, dan Volatility."
        )

    with st.container(border=True):
        st.markdown("### 🔥 Correlation Analysis")

        st.write(
            "Mengevaluasi hubungan antar fitur menggunakan "
            "matriks korelasi dan heatmap."
        )
