
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_processing import clean_data
from analysis import calculate_abc_analysis, calculate_rfm_analysis


st.set_page_config(
    page_title="BookFlow | B2B Sales Intelligence",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = Path(__file__).resolve().parent / "data" / "B2B_Transaction_Data_.xlsx"


@st.cache_data(show_spinner="Loading transaction data...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["Category"] = (
        df["Category"].fillna("Unknown").astype(str).str.strip()
    )
    return clean_data(df)


if not DATA_FILE.exists():
    st.error("Dataset not found. Please check the data directory.")
    st.stop()

try:
    df = load_data(str(DATA_FILE))
except Exception as exc:
    st.error(f"Unable to load dataset: {exc}")
    st.stop()


st.title("📚 BookFlow | B2B Sales Intelligence")
st.caption("ISL 467E | B2B Book Distributor | 2020 Transaction Analysis")


st.sidebar.header("Dashboard Filters")

categories = sorted(df["Category"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    categories
)

if selected_categories:
    df = df[df["Category"].isin(selected_categories)].copy()

if df.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()


st.header("Executive Overview")

total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products = df["StockCode"].nunique()

average_order_value = (
    total_revenue / total_orders if total_orders > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Average Order Value",
    f"{average_order_value:,.2f}"
)

st.caption(
    "Revenue is calculated as Quantity × NetPrice, "
    "assuming NetPrice represents the net unit price."
)


st.subheader("Monthly Sales Performance")

monthly_sales = (
    df.assign(
        Month=df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    )
    .groupby("Month", as_index=False)["Revenue"]
    .sum()
    .sort_values("Month")
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Net Sales Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Net Sales Revenue",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig_monthly, use_container_width=True)


st.subheader("Top 10 Product Categories")

category_sales = (
    df.groupby("Category", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig_categories = px.bar(
    category_sales,
    x="Revenue",
    y="Category",
    orientation="h",
    title="Top 10 Categories by Sales Revenue"
)

fig_categories.update_layout(
    xaxis_title="Net Sales Revenue",
    yaxis_title="Product Category",
    yaxis={
        "categoryorder": "total ascending"
    },
    template="plotly_white"
)

st.plotly_chart(fig_categories, use_container_width=True)


st.divider()

st.header("ABC Product Analysis")

st.write(
    "ABC analysis classifies products according to "
    "their contribution to total sales revenue."
)

abc_products = calculate_abc_analysis(df)

abc_summary = (
    abc_products.groupby("ABC_Class", as_index=False)
    .agg(
        Product_Count=("StockCode", "count"),
        Total_Revenue=("Total_Revenue", "sum")
    )
)

abc_summary["Revenue_Share"] = (
    abc_summary["Total_Revenue"]
    / abc_summary["Total_Revenue"].sum() * 100
)

abc_summary["Product_Share"] = (
    abc_summary["Product_Count"]
    / abc_summary["Product_Count"].sum() * 100
)

abc_summary["ABC_Class"] = pd.Categorical(
    abc_summary["ABC_Class"],
    categories=["A", "B", "C"],
    ordered=True
)

abc_summary = abc_summary.sort_values("ABC_Class")


fig_abc = px.bar(
    abc_summary,
    x="ABC_Class",
    y="Revenue_Share",
    text="Revenue_Share",
    category_orders={
        "ABC_Class": ["A", "B", "C"]
    },
    title="ABC Analysis - Revenue Contribution"
)

fig_abc.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_abc.update_layout(
    xaxis_title="ABC Class",
    yaxis_title="Share of Total Revenue (%)",
    yaxis_range=[0, 100],
    template="plotly_white"
)

st.plotly_chart(fig_abc, use_container_width=True)


st.subheader("ABC Classification Summary")

st.dataframe(
    abc_summary.round(2),
    use_container_width=True,
    hide_index=True
)


st.subheader("Product Distribution by ABC Class")

fig_distribution = px.bar(
    abc_summary,
    x="ABC_Class",
    y="Product_Count",
    text="Product_Count",
    category_orders={
        "ABC_Class": ["A", "B", "C"]
    },
    title="Number of Products by ABC Class"
)

fig_distribution.update_layout(
    xaxis_title="ABC Class",
    yaxis_title="Number of Products",
    template="plotly_white"
)

st.plotly_chart(fig_distribution, use_container_width=True)


st.divider()

st.header("Data Quality and Transaction Preview")

with st.expander("View Transaction Data"):
    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )

with st.expander("View Missing Values"):
    missing_values = (
        df.isna().sum().reset_index()
    )

    missing_values.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_values,
        use_container_width=True,
        hide_index=True
    )


st.divider()

st.header("RFM Customer Segmentation")

st.write(
    "Customers are segmented based on recency, "
    "purchase frequency, and total monetary value."
)

rfm = calculate_rfm_analysis(df)

segment_summary = (
    rfm.groupby("Segment", as_index=False)
    .agg(
        Customer_Count=("CustomerID", "count"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Frequency=("Frequency", "mean")
    )
)

segment_summary["Revenue_Share"] = (
    segment_summary["Total_Revenue"]
    / segment_summary["Total_Revenue"].sum() * 100
)

fig_rfm = px.bar(
    segment_summary,
    x="Segment",
    y="Customer_Count",
    color="Segment",
    text="Customer_Count",
    title="Customer Distribution by RFM Segment"
)

fig_rfm.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Number of Customers",
    showlegend=False,
    template="plotly_white"
)

st.plotly_chart(fig_rfm, use_container_width=True)

st.subheader("Customer Segment Performance")

st.dataframe(
    segment_summary.round(2),
    use_container_width=True,
    hide_index=True
)

st.subheader("Customer Revenue Contribution")

fig_segment_revenue = px.bar(
    segment_summary,
    x="Segment",
    y="Revenue_Share",
    color="Segment",
    text="Revenue_Share",
    title="Revenue Contribution by Customer Segment"
)

fig_segment_revenue.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_segment_revenue.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Share of Total Revenue (%)",
    showlegend=False,
    template="plotly_white"
)

st.plotly_chart(
    fig_segment_revenue,
    use_container_width=True
)
