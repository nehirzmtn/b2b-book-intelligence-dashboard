
# BookFlow – B2B Sales Intelligence Dashboard

An interactive business intelligence dashboard developed using Python and Streamlit for analyzing B2B book distribution transactions.

## Live Dashboard

[Open BookFlow Dashboard](https://b2b-book-intelligence-dashboard-p9vjcbudxtpdsaebsp7yu4.streamlit.app/)

## Project Overview

BookFlow provides data-driven insights for sales, marketing, and supply chain decision-making using a 2020 B2B transaction dataset.

## Dashboard Features

- **Executive Overview:** Sales KPIs, revenue trends, and category performance.
- **Sales & Marketing:** Customer segmentation using RFM analysis.
- **Supply Chain:** Product prioritization using ABC analysis.
- **Sales Forecasting:** Comparison of four forecasting models using MAE and RMSE.
- **Smart Insights:** Automatically generated business findings and recommendations.
- **Data Quality:** Data preprocessing report, missing values, and cleaning results.

## Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL

## Data Preprocessing

The original dataset contains 664,154 transaction records.

After cleaning, 664,138 records were retained and 16 records were removed due to missing, invalid, or non-positive essential values.

Revenue is calculated as Quantity × NetPrice, assuming NetPrice represents the net unit price.

## Analytical Methods

- ABC Classification
- RFM Customer Segmentation
- Time Series Forecasting
- Rule-Based Business Recommendations

## Forecasting Models

- Naive Forecast
- Moving Average (3 Months)
- Simple Linear Regression
- Multiple Linear Regression

The models are evaluated using MAE and RMSE. Forecast reliability is limited by the short historical period.

## How to Run Locally

1. Clone the repository.
2. Install dependencies:

    pip install -r requirements.txt

3. Start the dashboard:

    streamlit run streamlit_app.py

## Limitations

- The dataset covers only 2020.
- NetPrice is assumed to represent the net unit selling price.
- Identical transaction rows are retained because unique invoice-line identifiers are unavailable.
- ABC analysis uses revenue contribution rather than inventory levels.
- RFM segments are rule-based and do not constitute verified churn predictions.

## Course

Management Engineering Applications with Python – ISL467E
