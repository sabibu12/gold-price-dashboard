import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.load_data import load_data

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
    use_container_width=True
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
        st.caption("Deep learning models for time series forecasting")

with col3:
    with st.container(border=True):
        st.markdown("### ⚙️ Engineered Features")
        st.write("##### Lag, EMA, Momentum, Volatility, High Low Spread")
        st.caption("Features created to capture trends and volatility")

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

# =========================================================
# Load Data
# =========================================================
df = load_data()

# Daily Return
df["Daily_Return"] = (
    df["Close"].pct_change() * 100
)

# =========================================================
# HEADER
# =========================================================
st.title("📈 Price Analysis")

st.markdown("""
Halaman ini menampilkan analisis pergerakan harga emas
berdasarkan data historis Open, High, Low, dan Close.
""")

# =========================================================
# FILTER
# =========================================================
st.sidebar.header("🔍 Filter Data")

selected_price = st.sidebar.selectbox(
    "Pilih Harga",
    ["Close", "Open", "High", "Low"]
)

# =========================================================
# OHLC TREND
# =========================================================
st.subheader("📊 OHLC Price Trend")

fig_ohlc = px.line(
    df,
    x="Date",
    y=["Open", "High", "Low", "Close"],
    title="Pergerakan Harga OHLC"
)

fig_ohlc.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga"
)

st.plotly_chart(
    fig_ohlc,
    use_container_width=True
)

# =========================================================
# CANDLESTICK
# =========================================================
st.subheader("🕯️ Candlestick Chart")

fig_candle = go.Figure(
    data=[
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )
    ]
)

fig_candle.update_layout(
    title="Candlestick Harga Emas",
    xaxis_title="Tanggal",
    yaxis_title="Harga"
)

st.plotly_chart(
    fig_candle,
    use_container_width=True
)

# =========================================================
# DAILY RETURN DISTRIBUTION
# =========================================================
st.subheader("📉 Distribusi Daily Return")

fig_return = px.histogram(
    df,
    x="Daily_Return",
    nbins=50,
    title="Distribusi Daily Return"
)

fig_return.update_layout(
    xaxis_title="Daily Return (%)",
    yaxis_title="Frekuensi"
)

st.plotly_chart(
    fig_return,
    use_container_width=True
)

# =========================================================
# EMA ANALYSIS
# =========================================================
st.subheader("📈 EMA Analysis")

fig_ema = px.line(
    df,
    x="Date",
    y=["Close", "EMA_7", "EMA_30"],
    title="Close Price vs EMA"
)

fig_ema.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga"
)

st.plotly_chart(
    fig_ema,
    use_container_width=True
)

# =========================================================
# VOLATILITY
# =========================================================
st.subheader("🔥 Volatility Analysis")

fig_vol = px.line(
    df,
    x="Date",
    y=["Volatility_7", "Volatility_30"],
    title="Volatility 7 vs 30"
)

fig_vol.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Volatility"
)

st.plotly_chart(
    fig_vol,
    use_container_width=True
)

# =========================================================
# INSIGHT
# =========================================================
st.subheader("💡 Insight")

with st.container(border=True):

    st.markdown("""
    - Harga emas menunjukkan tren meningkat dalam jangka panjang.
    - EMA 7 lebih responsif terhadap perubahan harga dibanding EMA 30.
    - Volatility 30 cenderung lebih stabil dibanding Volatility 7.
    - Distribusi return harian menunjukkan sebagian besar perubahan harga
      berada di sekitar nol dengan beberapa lonjakan ekstrem.
    """)

# =========================================================
# LOAD DATA
# =========================================================
df = load_data()

# =========================================================
# HEADER
# =========================================================
st.title("🔥 Correlation Analysis")

st.markdown("""
Halaman ini menampilkan hubungan antar fitur
menggunakan analisis korelasi.
""")

# =========================================================
# CORRELATION MATRIX
# =========================================================
st.subheader("📊 Correlation Heatmap")

corr_matrix = (
    df.select_dtypes(include="number")
    .corr()
)

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect="auto",
    title="Correlation Matrix"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# =========================================================
# CORRELATION TO CLOSE
# =========================================================
st.subheader("📈 Korelasi terhadap Close")

corr_close = (
    corr_matrix["Close"]
    .drop("Close")
    .sort_values(ascending=True)
)

fig_corr = px.bar(
    corr_close,
    orientation="h",
    title="Korelasi Fitur terhadap Close"
)

fig_corr.update_layout(
    xaxis_title="Nilai Korelasi",
    yaxis_title="Fitur"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# =========================================================
# SCATTER PLOT
# =========================================================
st.subheader("🔍 Scatter Plot Analysis")

feature_x = st.selectbox(
    "Pilih Feature X",
    corr_close.index
)

fig_scatter = px.scatter(
    df,
    x=feature_x,
    y="Close",
    trendline="ols",
    title=f"{feature_x} vs Close"
)

fig_scatter.update_layout(
    xaxis_title=feature_x,
    yaxis_title="Close"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# =========================================================
# TOP CORRELATED FEATURES
# =========================================================
st.subheader("⭐ Top Correlated Features")

top_corr = (
    corr_close
    .abs()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

top_corr.columns = [
    "Feature",
    "Correlation"
]

st.dataframe(
    top_corr,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# INSIGHT
# =========================================================
st.subheader("💡 Insight")

top_feature = top_corr.iloc[0]["Feature"]
top_value = top_corr.iloc[0]["Correlation"]

with st.container(border=True):

    st.markdown(
        f"""
        - Fitur dengan korelasi tertinggi terhadap Close adalah
          **{top_feature}** dengan nilai korelasi
          **{top_value:.3f}**.
          
        - Lag Features dan EMA menunjukkan hubungan kuat
          terhadap harga penutupan emas.
          
        - Volatility memiliki korelasi lebih rendah karena
          mengukur tingkat fluktuasi harga, bukan arah tren.
        """
    )
