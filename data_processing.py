
import pandas as pd


def clean_data(df):
    # Create a copy of the original dataset
    cleaned = df.copy()

    # Convert the invoice date to datetime
    cleaned["InvoiceDate"] = pd.to_datetime(
        cleaned["InvoiceDate"],
        errors="coerce"
    )

    # Convert numeric columns to numeric values
    for col in ["Quantity", "NetPrice", "UnitPrice"]:
        cleaned[col] = pd.to_numeric(
            cleaned[col],
            errors="coerce"
        )

    # Replace placeholder city values with missing values
    cleaned["City"] = cleaned["City"].replace(
        ["NULL", "", "nan"],
        pd.NA
    )

    # Remove rows with missing essential values
    cleaned = cleaned.dropna(
        subset=[
            "InvoiceDate",
            "Quantity",
            "NetPrice",
            "UnitPrice"
        ]
    )

    # Keep positive sales transactions
    cleaned = cleaned[
        (cleaned["Quantity"] > 0) &
        (cleaned["NetPrice"] > 0)
    ].copy()

    # Calculate revenue using net unit price
    cleaned["Revenue"] = (
        cleaned["Quantity"] * cleaned["NetPrice"]
    )

    return cleaned
