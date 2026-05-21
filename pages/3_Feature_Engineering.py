import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# =========================
# Load Data
# =========================
df = load_data()

# =========================
# Header
# =========================
st.title("⚙️ Feature Engineering")

st.markdown("""
Halaman ini menampilkan proses rekayasa fitur (*feature engineering*)
yang dilakukan untuk menangkap pola historis harga emas sebelum
digunakan pada model forecasting berbasis **LSTM** dan **GRU**.
""")

# =========================
# Ringkasan Feature Engineering
# =========================
st.subheader("📋 Ringkasan Feature Engineering")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(
            "Jumlah Fitur Awal",
            5
        )

        st.caption(
            "Open, High, Low, Close, dan Volume"
        )

with col2:
    with st.container(border=True):
        st.metric(
            "Jumlah Fitur Akhir",
            13
        )

        st.caption(
            "Fitur hasil seleksi yang digunakan untuk pemodelan"
        )

# =========================
# Tahapan Feature Engineering
# =========================
st.subheader("🔄 Tahapan Rekayasa Fitur")

with st.container(border=True):
    st.markdown("""
    1. Mengubah tipe data kolom tanggal menjadi format datetime.
    2. Membuat fitur **Lag_1**, **Lag_7**, dan **Lag_30**.
    3. Membuat fitur **Moving Average (MA)** dan **Exponential Moving Average (EMA)**.
    4. Membuat fitur **Volatility** untuk mengukur fluktuasi harga.
    5. Membuat fitur **Momentum** untuk melihat arah pergerakan harga.
    6. Membuat fitur **High-Low Spread** sebagai ukuran rentang harga harian.
    7. Melakukan seleksi fitur berdasarkan korelasi terhadap target.
    """)

# =========================
# Lag Features
# =========================
st.subheader("📈 Lag Features")

selected_lag = st.selectbox(
    "Pilih Lag Feature",
    ["Lag_1", "Lag_7", "Lag_30"]
)

fig_lag = px.line(
    df,
    x="Date",
    y=["Close", selected_lag],
    title=f"Perbandingan Close dan {selected_lag}"
)

fig_lag.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga"
)

st.plotly_chart(
    fig_lag,
    use_container_width=True
)

st.caption(
    "Lag feature digunakan untuk menangkap pengaruh harga pada periode sebelumnya terhadap harga saat ini."
)

# =========================
# EMA
# =========================
st.subheader("📊 Exponential Moving Average (EMA)")

fig_ema = px.line(
    df,
    x="Date",
    y=["Close", "EMA_7", "EMA_30"],
    title="Perbandingan Close, EMA 7 Hari, dan EMA 30 Hari"
)

fig_ema.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga"
)

st.plotly_chart(
    fig_ema,
    use_container_width=True
)

st.caption(
    "EMA memberikan bobot lebih besar pada data terbaru sehingga lebih responsif terhadap perubahan tren."
)

# =========================
# Volatility
# =========================
st.subheader("📉 Volatility")

selected_volatility = st.selectbox(
    "Pilih Periode Volatility",
    ["Volatility_7", "Volatility_30"]
)

fig_vol = px.line(
    df,
    x="Date",
    y=selected_volatility,
    title=f"{selected_volatility} dari Waktu ke Waktu"
)

fig_vol.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Nilai Volatility"
)

st.plotly_chart(
    fig_vol,
    use_container_width=True
)

st.caption(
    "Volatility menunjukkan tingkat fluktuasi harga dalam periode tertentu. Semakin tinggi nilainya, semakin besar pergerakan harga yang terjadi."
)

# =========================
# Momentum
# =========================
st.subheader("🚀 Momentum")

fig_momentum = px.line(
    df,
    x="Date",
    y="Momentum_30",
    title="Momentum 30 Hari"
)

fig_momentum.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Momentum"
)

st.plotly_chart(
    fig_momentum,
    use_container_width=True
)

st.caption(
    "Momentum digunakan untuk mengukur kekuatan dan arah tren harga dibandingkan periode sebelumnya."
)

# =========================
# Korelasi Fitur
# =========================
st.subheader("📊 Korelasi Fitur terhadap Close")

corr_df = (
    df
    .corr(numeric_only=True)["Close"]
    .drop("Close")
    .abs()
    .sort_values(ascending=True)
)

fig_corr = px.bar(
    corr_df,
    orientation="h",
    title="Korelasi Fitur terhadap Harga Penutupan (Close)"
)

fig_corr.update_layout(
    xaxis_title="Nilai Korelasi",
    yaxis_title="Fitur"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

top_feature = corr_df.idxmax()
top_corr = corr_df.max()

with st.container(border=True):
    st.markdown(
        f"""
        **Insight:**

        Fitur yang memiliki korelasi tertinggi terhadap harga penutupan (**Close**)
        adalah **{top_feature}** dengan nilai korelasi sebesar **{top_corr:.3f}**.
        Nilai korelasi yang tinggi menunjukkan bahwa fitur tersebut memiliki hubungan
        yang kuat dengan perubahan harga emas.
        """
    )

# =========================
# Dataset Preview
# =========================
st.subheader("🔍 Dataset Hasil Feature Engineering")

preview_df = df.copy()

preview_df["Date"] = (
    preview_df["Date"]
    .dt.strftime("%Y-%m-%d")
)

cols = ["Date"] + [
    col for col in preview_df.columns
    if col != "Date"
]

preview_df = preview_df[cols]

st.dataframe(
    preview_df.tail(10),
    use_container_width=True
)