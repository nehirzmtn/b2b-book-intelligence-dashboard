
import numpy as np
import pandas as pd


def predict_future(history, model_name, periods=3):
    history = np.asarray(history, dtype=float)
    predictions = []
    simulated_history = history.tolist()

    if model_name == "Simple Linear Regression":
        x = np.arange(len(history))
        coefficients = np.polyfit(x, history, 1)

    elif model_name == "Multiple Linear Regression":
        x = np.column_stack([
            np.ones(len(history) - 1),
            np.arange(1, len(history)),
            history[:-1]
        ])
        y = history[1:]

        coefficients = np.linalg.lstsq(
            x, y, rcond=None
        )[0]

    for _ in range(periods):
        next_month = len(simulated_history)

        if model_name == "Naive Forecast":
            prediction = simulated_history[-1]

        elif model_name == "Moving Average (3 Months)":
            prediction = np.mean(simulated_history[-3:])

        elif model_name == "Simple Linear Regression":
            prediction = np.polyval(
                coefficients, next_month
            )

        elif model_name == "Multiple Linear Regression":
            prediction = (
                coefficients[0]
                + coefficients[1] * next_month
                + coefficients[2] * simulated_history[-1]
            )

        else:
            raise ValueError("Unknown forecasting model.")

        prediction = max(float(prediction), 0.0)
        predictions.append(prediction)
        simulated_history.append(prediction)

    return np.array(predictions)


def calculate_sales_forecast(df, forecast_periods=3):
    # Aggregate revenue by calendar month
    monthly = (
        df.assign(
            Month=df["InvoiceDate"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby("Month")["Revenue"]
        .sum()
        .sort_index()
        .asfreq("MS", fill_value=0)
    )

    if len(monthly) < 9:
        raise ValueError(
            "At least nine months of data are required."
        )

    values = monthly.to_numpy(dtype=float)

    # Use the last three months as the test period
    train = values[:-3]
    test = values[-3:]

    models = [
        "Naive Forecast",
        "Moving Average (3 Months)",
        "Simple Linear Regression",
        "Multiple Linear Regression"
    ]

    evaluation_results = []

    # Compare models on the same test period
    for model in models:
        predictions = predict_future(
            train,
            model,
            periods=len(test)
        )

        mae = np.mean(np.abs(test - predictions))
        rmse = np.sqrt(
            np.mean((test - predictions) ** 2)
        )

        evaluation_results.append({
            "Model": model,
            "MAE": mae,
            "RMSE": rmse
        })

    evaluation = (
        pd.DataFrame(evaluation_results)
        .sort_values("MAE")
        .reset_index(drop=True)
    )

    # Select the model with the lowest validation MAE
    best_model = evaluation.loc[0, "Model"]

    # Refit the selected model using all available months
    future_values = predict_future(
        values,
        best_model,
        periods=forecast_periods
    )

    future_dates = pd.date_range(
        start=monthly.index[-1] + pd.offsets.MonthBegin(1),
        periods=forecast_periods,
        freq="MS"
    )

    forecast = pd.DataFrame({
        "Month": future_dates,
        "Forecast_Revenue": future_values
    })

    historical = monthly.reset_index()
    historical.columns = ["Month", "Revenue"]

    return historical, forecast, evaluation, best_model
