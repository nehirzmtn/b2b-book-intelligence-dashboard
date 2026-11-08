
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_processing import clean_data
from analysis import calculate_abc_analysis, calculate_rfm_analysis
from forecasting import calculate_sales_forecast, predict_future
from business_insights import generate_business_insights


st.set_page_config(
    page_title="BookFlow | B2B Sales Intelligence",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "B2B_Transaction_Data_.xlsx"
)


@st.cache_data(show_spinner="Loading transaction data...")
def load_data(path):
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["Category"] = (
        df["Category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )
    return clean_data(df)


def display_overview(df):
    st.header("Executive Overview")
    st.write("Key sales performance indicators and revenue trends.")

    revenue = df["Revenue"].sum()
    orders = df["InvoiceNo"].nunique()
    customers = df["CustomerID"].nunique()
    products = df["StockCode"].nunique()
    aov = revenue / orders if orders else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"{revenue:,.2f}")
    c2.metric("Total Orders", f"{orders:,}")
    c3.metric("Active Customers", f"{customers:,}")
    c4.metric("Average Order Value", f"{aov:,.2f}")

    st.caption(
        "Revenue is calculated as Quantity × NetPrice, "
        "assuming NetPrice represents the net unit price."
    )

    monthly = (
        df.assign(
            Month=df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("Month", as_index=False)["Revenue"]
        .sum()
        .sort_values("Month")
    )

    st.subheader("Monthly Sales Performance")

    fig = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Net Sales Revenue"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Net Sales Revenue",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Product Categories")

    categories = (
        df.groupby("Category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig = px.bar(
        categories,
        x="Revenue",
        y="Category",
        orientation="h",
        title="Top Categories by Revenue"
    )
    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"}
    )
    st.plotly_chart(fig, use_container_width=True)


def display_marketing(df):
    st.header("Sales & Marketing")
    st.write(
        "Customer segmentation using Recency, "
        "Frequency, and Monetary Value."
    )

    rfm = calculate_rfm_analysis(df)

    summary = (
        rfm.groupby("Segment", as_index=False)
        .agg(
            Customer_Count=("CustomerID", "count"),
            Total_Revenue=("Monetary", "sum"),
            Avg_Frequency=("Frequency", "mean")
        )
    )

    summary["Revenue_Share"] = (
        summary["Total_Revenue"]
        / summary["Total_Revenue"].sum() * 100
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Customers Analyzed", f"{len(rfm):,}")
    c2.metric(
        "Champions",
        f"{(rfm['Segment'] == 'Champions').sum():,}"
    )
    c3.metric(
        "At Risk Customers",
        f"{(rfm['Segment'] == 'At Risk').sum():,}"
    )

    st.subheader("Customer Segmentation")

    fig = px.bar(
        summary,
        x="Segment",
        y="Customer_Count",
        color="Segment",
        text="Customer_Count",
        title="Customer Distribution by RFM Segment"
    )
    fig.update_layout(
        showlegend=False,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Revenue Contribution")

    fig = px.bar(
        summary,
        x="Segment",
        y="Revenue_Share",
        color="Segment",
        text="Revenue_Share",
        title="Revenue Share by Customer Segment"
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
    fig.update_layout(
        showlegend=False,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Segment Summary")
    st.dataframe(
        summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Customer segments are based on rule-based RFM scores. "
        "The At Risk label does not represent a verified churn prediction."
    )


def display_supply_chain(df):
    st.header("Supply Chain & Product Analysis")
    st.write(
        "Product prioritization based on ABC revenue classification."
    )

    abc = calculate_abc_analysis(df)

    summary = (
        abc.groupby("ABC_Class", as_index=False)
        .agg(
            Product_Count=("StockCode", "count"),
            Total_Revenue=("Total_Revenue", "sum")
        )
    )

    summary["Revenue_Share"] = (
        summary["Total_Revenue"]
        / summary["Total_Revenue"].sum() * 100
    )
    summary["Product_Share"] = (
        summary["Product_Count"]
        / summary["Product_Count"].sum() * 100
    )

    summary["ABC_Class"] = pd.Categorical(
        summary["ABC_Class"],
        categories=["A", "B", "C"],
        ordered=True
    )
    summary = summary.sort_values("ABC_Class")

    st.subheader("ABC Revenue Contribution")

    fig = px.bar(
        summary,
        x="ABC_Class",
        y="Revenue_Share",
        text="Revenue_Share",
        title="Revenue Contribution by ABC Class"
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
    fig.update_layout(
        template="plotly_white",
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Product Distribution")

    fig = px.bar(
        summary,
        x="ABC_Class",
        y="Product_Count",
        text="Product_Count",
        title="Number of Products by ABC Class"
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("ABC Classification Summary")
    st.dataframe(
        summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "ABC classes represent revenue contribution. "
        "Inventory levels and replenishment lead times "
        "are not available in this dataset."
    )


def display_forecasting(df):
    st.header("Sales Forecasting")
    st.write(
        "Comparison of Naive Forecast, Moving Average, "
        "Simple Linear Regression, and Multiple Linear Regression."
    )

    try:
        historical, default_forecast, evaluation, best_model = (
            calculate_sales_forecast(df)
        )

        selected_model = st.selectbox(
            "Select Forecasting Model",
            evaluation["Model"].tolist(),
            index=0
        )

        predictions = predict_future(
            historical["Revenue"].to_numpy(),
            selected_model,
            periods=3
        )

        forecast = default_forecast.copy()
        forecast["Forecast_Revenue"] = predictions

        best_mae = evaluation.loc[
            evaluation["Model"] == best_model, "MAE"
        ].iloc[0]

        selected_mae = evaluation.loc[
            evaluation["Model"] == selected_model, "MAE"
        ].iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Best Performing Model", best_model)
        c2.metric("Best Validation MAE", f"{best_mae:,.2f}")
        c3.metric("Selected Model MAE", f"{selected_mae:,.2f}")

        st.subheader("Historical Sales and Forecast")

        fig = px.line(
            historical,
            x="Month",
            y="Revenue",
            markers=True,
            title=f"Sales Forecast - {selected_model}"
        )

        fig.update_traces(
            name="Historical Sales",
            showlegend=True
        )

        forecast_months = pd.concat(
            [historical["Month"].tail(1), forecast["Month"]],
            ignore_index=True
        )
        forecast_values = pd.concat(
            [
                historical["Revenue"].tail(1),
                forecast["Forecast_Revenue"]
            ],
            ignore_index=True
        )

        fig.add_scatter(
            x=forecast_months,
            y=forecast_values,
            mode="lines+markers",
            name="Forecast",
            line=dict(color="#EF553B", dash="dash", width=3)
        )

        fig.add_vline(
            x=historical["Month"].iloc[-1].timestamp() * 1000,
            line_dash="dot",
            line_color="gray"
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Month",
            yaxis_title="Net Sales Revenue",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Model Evaluation")
        st.dataframe(
            evaluation.round(2),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Forecasted Monthly Revenue")
        st.dataframe(
            forecast.round(2),
            use_container_width=True,
            hide_index=True
        )

        if selected_model == best_model:
            st.success(
                f"{selected_model} achieved the lowest validation MAE."
            )
        else:
            st.info(
                f"{best_model} achieved a lower validation MAE "
                f"than {selected_model}."
            )

        st.caption(
            "Models are evaluated on October-December 2020. "
            "Forecasts cover January-March 2021. "
            "The 12-month history limits forecast reliability."
        )

    except (ValueError, TypeError, IndexError) as exc:
        st.warning(f"Forecast unavailable: {exc}")


def display_insights(df):
    st.header("Smart Business Insights")
    st.write(
        "Automatically generated findings and recommended "
        "actions for business decision-making."
    )

    abc = calculate_abc_analysis(df)
    rfm = calculate_rfm_analysis(df)

    try:
        _, _, evaluation, _ = calculate_sales_forecast(df)
    except ValueError:
        evaluation = None

    insights = generate_business_insights(
        df=df,
        abc_products=abc,
        rfm=rfm,
        evaluation=evaluation
    )

    if not insights:
        st.info("No insights are available for the selected data.")
        return

    departments = ["All Departments"] + sorted(
        {item["Department"] for item in insights}
    )

    selected_department = st.selectbox(
        "Filter Insights by Department",
        departments
    )

    for item in insights:
        if (
            selected_department != "All Departments"
            and item["Department"] != selected_department
        ):
            continue

        with st.container(border=True):
            st.caption(item["Department"])
            st.subheader(item["Title"])
            st.write(item["Finding"])
            st.markdown(
                "**Recommended Action:** "
                + item["Recommendation"]
            )


def display_data_quality(df):
    with st.expander("Data Preview and Quality"):
        st.subheader("Transaction Preview")
        st.dataframe(
            df.head(100),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Missing Values in Analysis Dataset")
        missing = df.isna().sum().reset_index()
        missing.columns = ["Column", "Missing Values"]

        st.dataframe(
            missing,
            use_container_width=True,
            hide_index=True
        )


def main():
    if not DATA_FILE.exists():
        st.error("Dataset not found in the data directory.")
        st.stop()

    try:
        df = load_data(str(DATA_FILE))
    except Exception as exc:
        st.error(f"Unable to load data: {exc}")
        st.stop()

    st.sidebar.title("📚 BookFlow")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Overview",
            "Sales & Marketing",
            "Supply Chain",
            "Sales Forecasting",
            "Smart Insights"
        ]
    )

    st.sidebar.divider()
    st.sidebar.subheader("Dashboard Filters")

    categories = sorted(df["Category"].dropna().unique())

    selected_categories = st.sidebar.multiselect(
        "Product Categories",
        categories
    )

    if selected_categories:
        df = df[df["Category"].isin(selected_categories)].copy()

    if df.empty:
        st.warning("No transactions match the selected filters.")
        st.stop()

    st.title("BookFlow | B2B Sales Intelligence")
    st.caption(
        "ISL 467E | Management Engineering Applications with Python"
    )

    if page == "Executive Overview":
        display_overview(df)

    elif page == "Sales & Marketing":
        display_marketing(df)

    elif page == "Supply Chain":
        display_supply_chain(df)

    elif page == "Sales Forecasting":
        display_forecasting(df)

    elif page == "Smart Insights":
        display_insights(df)

    display_data_quality(df)


if __name__ == "__main__":
    main()
