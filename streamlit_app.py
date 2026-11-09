
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
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], [data-testid="stApp"] {
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: #F6F8FC;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #142D45;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2 {
        color: #142D45;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h3 {
        color: #263F56;
        font-weight: 650;
    }

    p {
        line-height: 1.6;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 3px 12px rgba(20, 45, 69, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #748395;
        font-size: 0.9rem;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #142D45;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.6px;
    }

    section[data-testid="stSidebar"] {
    background: #EDF2F8;
    border-right: 1px solid #D9E3ED;
}

section[data-testid="stSidebar"] > div {
    background: #EDF2F8;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 10px 12px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #DEE8F2;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #D7E6F0;
    border: 1px solid #C2D7E5;
    font-weight: 650;
}

    section[data-testid="stSidebar"] h1 {
        color: #142D45;
        font-size: 1.5rem;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        border-radius: 9px;
        padding: 7px 9px;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #F0F5F9;
    }

    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 16px;
        padding: 12px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E1E8F0;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    hr {
        border-color: #E1E8F0;
    }
    [data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 38px;
    padding: 7px 12px;
    border-radius: 8px;
    justify-content: flex-start;
    text-align: left;
    font-size: 0.86rem;
    font-weight: 500;
    box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: transparent;
    color: #41566D;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: #DFE9F2;
    color: #17324D;
    border-color: transparent;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #17324D;
    color: #FFFFFF;
    border: 1px solid #17324D;
    font-weight: 650;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #244B6A;
    border-color: #244B6A;
}

[data-testid="stSidebar"] .stButton {
    margin-bottom: 2px;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: none;
    background: transparent;
}

[data-testid="stSidebar"] .stMultiSelect > div {
    border-radius: 9px;
}

[data-testid="stSidebar"] .stDateInput > div {
    border-radius: 9px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 42px;
    border-radius: 9px;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #17324D;
}
/* Sidebar filter styling */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #41566D;
    font-size: 0.85rem;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border: 1px solid #D9E2EC;
    border-radius: 10px;
    min-height: 42px;
}

[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background-color: #FFFFFF;
    border-radius: 10px;
    color: #17324D;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background-color: #FFFFFF;
    color: #17324D;
    border: 1px solid #C9D7E5;
    border-radius: 10px;
    font-weight: 600;
}

[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background-color: #E0EAF3;
    border-color: #17324D;
}

.brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0 18px;
    margin-bottom: 12px;
    border-bottom: 1px solid #D4E0EA;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 11px;
    background: #17324D;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    flex-shrink: 0;
}

.brand-title {
    color: #17324D;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1.2;
}

.brand-subtitle {
    color: #718396;
    font-size: 0.75rem;
    margin-top: 4px;
}
/* Match Streamlit header with dashboard background */
[data-testid="stHeader"] {
    background-color: #F6F8FC !important;
    box-shadow: none !important;
    border-bottom: none !important;
}

[data-testid="stToolbar"] {
    background-color: transparent !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}
    </style>
    """,
    unsafe_allow_html=True
)

import plotly.io as pio

pio.templates["bookflow"] = pio.templates["plotly_white"]
pio.templates["bookflow"].layout.font.family = "DM Sans, sans-serif"
pio.templates["bookflow"].layout.font.color = "#263F56"
pio.templates["bookflow"].layout.colorway = [
    "#0D9488",
    "#2563EB",
    "#8B5CF6",
    "#F59E0B",
    "#EF6461",
    "#64748B"
]
pio.templates["bookflow"].layout.paper_bgcolor = "#FFFFFF"
pio.templates["bookflow"].layout.plot_bgcolor = "#FFFFFF"

pio.templates.default = "bookflow"
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
        template="bookflow",
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
        template="bookflow",
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
        template="bookflow"
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
        template="bookflow"
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
        template="bookflow",
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
    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="outside"
    )

    fig.update_layout(template="bookflow")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("ABC Classification Summary")
    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ABC_Class": st.column_config.TextColumn("ABC Class"),
            "Product_Count": st.column_config.NumberColumn(
                "Product Count", format="%d"
            ),
            "Total_Revenue": st.column_config.NumberColumn(
                "Total Revenue", format="%.2f"
            ),
            "Revenue_Share": st.column_config.NumberColumn(
                "Revenue Share (%)", format="%.2f"
            ),
            "Product_Share": st.column_config.NumberColumn(
                "Product Share (%)", format="%.2f"
            ),
        }
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
            template="bookflow",
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

@st.cache_data(show_spinner="Preparing data cleaning report...")
def load_cleaning_report(path):
    original = pd.read_excel(path, engine="openpyxl")
    cleaned = clean_data(original)

    invoice_dates = pd.to_datetime(
        original["InvoiceDate"], errors="coerce"
    )
    quantities = pd.to_numeric(
        original["Quantity"], errors="coerce"
    )
    net_prices = pd.to_numeric(
        original["NetPrice"], errors="coerce"
    )
    unit_prices = pd.to_numeric(
        original["UnitPrice"], errors="coerce"
    )

    valid_required = (
        invoice_dates.notna()
        & quantities.notna()
        & net_prices.notna()
        & unit_prices.notna()
    )

    missing_required = int((~valid_required).sum())

    nonpositive_sales = int((
        valid_required
        & ((quantities <= 0) | (net_prices <= 0))
    ).sum())

    missing_values = original.isna().sum().reset_index()
    missing_values.columns = ["Column", "Missing Values"]

    return {
        "original": len(original),
        "cleaned": len(cleaned),
        "missing_required": missing_required,
        "nonpositive_sales": nonpositive_sales,
        "missing_values": missing_values
    }

    
def display_cleaning_report(path):
    st.header("Data Quality & Cleaning Report")
    st.write(
        "Data preprocessing results and transaction quality overview."
    )

    report = load_cleaning_report(path)

    original = report["original"]
    cleaned = report["cleaned"]
    removed = original - cleaned
    retention = (cleaned / original * 100) if original else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Original Records", f"{original:,}")
    c2.metric("Cleaned Records", f"{cleaned:,}")
    c3.metric("Removed Records", f"{removed:,}")
    c4.metric("Retention Rate", f"{retention:.4f}%")

    st.subheader("Cleaning Breakdown")

    breakdown = pd.DataFrame({
        "Cleaning Step": [
            "Missing or invalid required values",
            "Non-positive quantity or net price"
        ],
        "Removed Rows": [
            report["missing_required"],
            report["nonpositive_sales"]
        ]
    })

    st.dataframe(
        breakdown,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Missing Values in Original Data")

    st.dataframe(
        report["missing_values"],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Missing-value counts reflect original null values. "
        "Text placeholders such as NULL may require separate checks."
    )

    st.subheader("Applied Cleaning Steps")

    st.markdown(
        """
        - Converted invoice dates to datetime.
        - Converted quantity and price columns to numeric.
        - Standardized placeholder city values as missing.
        - Removed rows with invalid essential values.
        - Excluded non-positive sales transactions.
        - Calculated revenue as Quantity × NetPrice.
        """
    )

    st.caption(
        "The report summarizes the full dataset before dashboard filters. "
        "Duplicate transactions are not automatically removed."
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

    st.sidebar.markdown(
        """
        <div class="brand-header">
            <div class="brand-icon">B</div>
            <div class="brand-text">
                <div class="brand-title">BookFlow</div>
                <div class="brand-subtitle">Analytics Workspace</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    if "current_page" not in st.session_state:
        st.session_state.current_page = "Executive Overview"

    st.sidebar.caption("WORKSPACE")

    navigation_items = {
        "Executive Overview": "▦  Executive Overview",
        "Sales & Marketing": "♧  Sales & Marketing",
        "Supply Chain": "▤  Supply Chain",
        "Sales Forecasting": "↗  Sales Forecasting",
        "Smart Insights": "✦  Smart Insights",
        "Data Quality": "✓  Data Quality"
    }

    for page_name, label in navigation_items.items():
        is_active = st.session_state.current_page == page_name

        if st.sidebar.button(
            label,
            key=f"nav_{page_name}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            st.session_state.current_page = page_name
            st.rerun()

    page = st.session_state.current_page


    st.sidebar.divider()
    st.sidebar.markdown("#### FILTERS")

    categories = sorted(
        df["Category"].dropna().unique().tolist()
    )

    cities = sorted(
        df["City"].dropna().astype(str).unique().tolist()
    )

    min_date = df["InvoiceDate"].min().date()
    max_date = df["InvoiceDate"].max().date()

    if st.session_state.get("reset_filters", False):
        st.session_state["selected_categories"] = []
        st.session_state["selected_cities"] = []
        st.session_state["start_date"] = min_date
        st.session_state["end_date"] = max_date
        st.session_state["reset_filters"] = False

    selected_categories = st.sidebar.multiselect(
        "Product Categories",
        options=categories,
        placeholder="All Categories",
        key="selected_categories"
    )

    selected_cities = st.sidebar.multiselect(
        "Cities",
        options=cities,
        placeholder="All Cities",
        key="selected_cities"
    )

    start_date = st.sidebar.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="start_date"
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="end_date"
    )

    def reset_dashboard_filters():
        st.session_state["reset_filters"] = True

    st.sidebar.button(
        "Reset Filters",
        on_click=reset_dashboard_filters,
        use_container_width=True,
        type="primary"
    )

    if selected_categories:
        df = df[df["Category"].isin(selected_categories)].copy()

    if selected_cities:
        df = df[df["City"].isin(selected_cities)].copy()

    if start_date <= end_date:
        df = df[
            (df["InvoiceDate"].dt.date >= start_date)
            & (df["InvoiceDate"].dt.date <= end_date)
        ].copy()
    else:
        st.warning("Start Date cannot be later than End Date.")
        st.stop()

    st.sidebar.caption("OVERVIEW & ANALYTICS")
    st.sidebar.metric(
        "Transactions",
        f"{len(df):,}"
    )

    st.sidebar.caption(
        "2020 B2B transaction dataset"
    )

    if df.empty:
        st.warning("No transactions match the selected filters.")
        st.stop()

    st.title("BookFlow")
    st.markdown(
        "**B2B Sales Intelligence & Decision Support Dashboard**"
    )
    st.caption(
        "Management Engineering Applications with Python "
        
    )
    st.divider()

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

    elif page == "Data Quality":
        display_cleaning_report(str(DATA_FILE))

    display_data_quality(df)


if __name__ == "__main__":
    main()
