
import pandas as pd


def generate_business_insights(
    df, abc_products, rfm, evaluation=None
):
    insights = []

    if df.empty:
        return insights

    total_revenue = df["Revenue"].sum()

    if total_revenue <= 0:
        return insights

    # Analyze customer revenue concentration
    champion_customers = rfm[
        rfm["Segment"] == "Champions"
    ]

    champion_count = len(champion_customers)

    champion_revenue = (
        champion_customers["Monetary"].sum()
    )

    champion_share = (
        champion_revenue / total_revenue * 100
    )

    insights.append({
        "Department": "Sales & Marketing",
        "Title": "Customer Revenue Concentration",
        "Finding": (
            f"{champion_count:,} Champion customers "
            f"generate {champion_share:.1f}% "
            "of total sales revenue."
        ),
        "Recommendation": (
            "Prioritize retention and personalized "
            "account management for high-value customers."
        )
    })

    # Identify customers with weaker recent engagement
    at_risk = rfm[rfm["Segment"] == "At Risk"]

    at_risk_count = len(at_risk)
    at_risk_share = (
        at_risk_count / len(rfm) * 100
    )

    insights.append({
        "Department": "Marketing",
        "Title": "Customer Re-engagement Opportunity",
        "Finding": (
            f"{at_risk_count:,} customers "
            f"({at_risk_share:.1f}%) are classified "
            "as At Risk based on their RFM scores."
        ),
        "Recommendation": (
            "Review customer purchase histories and "
            "consider targeted re-engagement campaigns."
        )
    })

    # Analyze ABC product concentration
    class_a = abc_products[
        abc_products["ABC_Class"] == "A"
    ]

    class_a_count = len(class_a)

    product_share = (
        class_a_count / len(abc_products) * 100
    )

    revenue_share = (
        class_a["Total_Revenue"].sum()
        / total_revenue * 100
    )

    insights.append({
        "Department": "Supply Chain",
        "Title": "Product Revenue Concentration",
        "Finding": (
            f"{product_share:.1f}% of products "
            f"generate {revenue_share:.1f}% "
            "of total sales revenue."
        ),
        "Recommendation": (
            "Prioritize demand planning and product "
            "availability reviews for Class A products."
        )
    })

    # Evaluate monthly sales performance
    monthly_sales = (
        df.assign(
            Month=df["InvoiceDate"].dt.to_period("M")
        )
        .groupby("Month")["Revenue"]
        .sum()
        .sort_index()
    )

    if len(monthly_sales) >= 2:
        latest_revenue = monthly_sales.iloc[-1]
        previous_revenue = monthly_sales.iloc[-2]

        if previous_revenue > 0:
            growth_rate = (
                (latest_revenue - previous_revenue)
                / previous_revenue * 100
            )

            trend = (
                "increased"
                if growth_rate >= 0
                else "decreased"
            )

            insights.append({
                "Department": "Sales",
                "Title": "Recent Sales Performance",
                "Finding": (
                    f"Monthly revenue {trend} by "
                    f"{abs(growth_rate):.1f}% "
                    "compared with the previous month."
                ),
                "Recommendation": (
                    "Review category-level demand "
                    "changes and investigate the main "
                    "drivers of recent sales performance."
                )
            })

    # Summarize forecasting model performance
    if evaluation is not None and not evaluation.empty:
        best = evaluation.loc[
            evaluation["MAE"].idxmin()
        ]

        insights.append({
            "Department": "Sales Planning",
            "Title": "Forecast Model Performance",
            "Finding": (
                f"{best['Model']} achieved the lowest "
                f"validation MAE of {best['MAE']:,.2f}."
            ),
            "Recommendation": (
                "Use the selected model as a planning "
                "baseline and monitor forecast errors "
                "as new transaction data becomes available."
            )
        })

    return insights
