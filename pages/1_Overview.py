import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_data

# Load Data
df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

period = st.sidebar.selectbox(
    "Quick Filter",
    ["All Time", "1 Year", "3 Years", "5 Years"]
)

max_date = df["Date"].max()

if period == "1 Year":
    min_date = max_date - pd.DateOffset(years=1)
elif period == "3 Years":
    min_date = max_date - pd.DateOffset(years=3)
elif period == "5 Years":
    min_date = max_date - pd.DateOffset(years=5)
else:
    min_date = df["Date"].min()

start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date.date(),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date.date(),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

selected_feature = st.sidebar.selectbox(
    "Price Type",
    ["Close", "Open", "High", "Low"]
)

# Filter Data
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
]

# Header
st.title("📈 Gold Price Dashboard")

st.markdown("""
Dashboard analisis harga emas berdasarkan data historis
dan hasil feature engineering untuk persiapan model LSTM & GRU.
""")

# KPI Calculation
latest_price = filtered_df["Close"].iloc[-1]
first_price = filtered_df["Close"].iloc[0]

price_change_pct = (
    (latest_price - first_price)
    / first_price
) * 100

highest_price = filtered_df["Close"].max()
lowest_price = filtered_df["Close"].min()
avg_price = filtered_df["Close"].mean()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Close Price",
    f"${latest_price:,.2f}",
    f"{price_change_pct:.2f}%"
)

col2.metric(
    "Highest Price",
    f"${highest_price:,.2f}"
)

col3.metric(
    "Lowest Price",
    f"${lowest_price:,.2f}"
)

col4.metric(
    "Average Price",
    f"${avg_price:,.2f}"
)

# Price Trend
st.subheader("📊 Price Trend")

fig = px.line(
    filtered_df,
    x="Date",
    y=selected_feature,
    title=f"{selected_feature} Price Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Monthly Average Price
st.subheader("📅 Monthly Average Price")
monthly_df = (
    filtered_df
    .set_index("Date")
    .resample("ME")["Close"]
    .mean()
    .reset_index()
)

fig_monthly = px.line(
    monthly_df,
    x="Date",
    y="Close",
    markers=True,
    title="Monthly Average Closing Price"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# Dataset Information
st.subheader("📋 Dataset Information")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Total Records",
    len(filtered_df)
)

info_col2.metric(
    "Start Date",
    str(filtered_df["Date"].min().date())
)

info_col3.metric(
    "End Date",
    str(filtered_df["Date"].max().date())
)

# Data Quality Summary
st.subheader("📊 Ringkasan Kualitas Data")

missing_values = filtered_df.isna().sum().sum()

duplicate_rows = filtered_df.duplicated().sum()

missing_percentage = (
    filtered_df.isna().sum().sum()
    / (filtered_df.shape[0] * filtered_df.shape[1])
) * 100

numeric_columns = len(
    filtered_df.select_dtypes(include="number").columns
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Missing Values",
    int(missing_values)
)

c2.metric(
    "Duplicate Rows",
    int(duplicate_rows)
)

c3.metric(
    "Missing (%)",
    f"{missing_percentage:.2f}%"
)

c4.metric(
    "Fitur Numerik",
    numeric_columns
)

with st.container(border=True):

    if missing_values == 0 and duplicate_rows == 0:
        st.success(
            "Dataset tidak memiliki missing values maupun data duplikat."
        )
    else:
        st.warning(
            "Dataset masih memerlukan pembersihan data lebih lanjut."
        )

# Descriptive Statistics
st.subheader("📈 Descriptive Statistics")

numeric_df = filtered_df.select_dtypes(
    include=["number"]
)

st.dataframe(
    numeric_df.describe(),
    use_container_width=True
)

# Data Preview
st.subheader("🔍 Data Preview")

preview_df = filtered_df.copy()

# Format tanggal
preview_df["Date"] = preview_df["Date"].dt.strftime("%Y-%m-%d")

# Pindahkan Date ke kolom pertama
cols = ["Date"] + [col for col in preview_df.columns if col != "Date"]
preview_df = preview_df[cols]

st.dataframe(
    preview_df.tail(),
    use_container_width=True
)