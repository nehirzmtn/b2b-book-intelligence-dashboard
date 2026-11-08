
import pandas as pd
import numpy as np


def calculate_abc_analysis(df):
    # Aggregate revenue and quantity by product
    product_sales = (
        df.groupby("StockCode", as_index=False)
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
    )

    # Sort products by revenue
    product_sales = product_sales.sort_values(
        "Total_Revenue", ascending=False
    ).reset_index(drop=True)

    # Calculate cumulative revenue contribution
    total_revenue = product_sales["Total_Revenue"].sum()

    product_sales["Cumulative_Percentage"] = (
        product_sales["Total_Revenue"].cumsum()
        / total_revenue * 100
    )

    previous_percentage = (
        product_sales["Cumulative_Percentage"]
        - product_sales["Total_Revenue"] / total_revenue * 100
    )

    # Assign ABC categories
    product_sales["ABC_Class"] = np.select(
        [
            previous_percentage < 80,
            previous_percentage < 95
        ],
        ["A", "B"],
        default="C"
    )

    return product_sales


def calculate_rfm_analysis(df):
    # Define the reference date
    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # Calculate customer-level RFM metrics
    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda x: (reference_date - x.max()).days
            ),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Revenue", "sum")
        )
        .reset_index()
    )

    # Calculate percentile-based RFM scores
    rfm["R_Score"] = np.ceil(
        (1 - rfm["Recency"].rank(pct=True, method="average")) * 5
    ).clip(1, 5).astype(int)

    rfm["F_Score"] = np.ceil(
        rfm["Frequency"].rank(pct=True, method="average") * 5
    ).clip(1, 5).astype(int)

    rfm["M_Score"] = np.ceil(
        rfm["Monetary"].rank(pct=True, method="average") * 5
    ).clip(1, 5).astype(int)

    # Calculate combined RFM score
    rfm["RFM_Score"] = (
        rfm["R_Score"] +
        rfm["F_Score"] +
        rfm["M_Score"]
    )

    # Assign customer segments
    def assign_segment(row):
        if (
            row["R_Score"] >= 4
            and row["F_Score"] >= 4
            and row["M_Score"] >= 4
        ):
            return "Champions"

        elif row["F_Score"] >= 4 and row["M_Score"] >= 3:
            return "Loyal Customers"

        elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
            return "At Risk"

        return "Other Customers"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    return rfm

