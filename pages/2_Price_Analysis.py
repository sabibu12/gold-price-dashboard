import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.load_data import load_data

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
