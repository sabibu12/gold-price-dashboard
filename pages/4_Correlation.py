import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

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
