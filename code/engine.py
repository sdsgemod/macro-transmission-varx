import yfinance as yf
import pandas as pd
import numpy as np
import warnings

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")

# -----------------------------
# DATA FETCH
# -----------------------------
def get_macro_data():
    assets = ['INR=X', '^TNX', '^NSEI', 'BZ=F']
    
    data = yf.download(
        assets,
        start="2020-01-01",
        end="2026-03-27",
        auto_adjust=True,
        progress=False
    )

    df = data['Close'].copy()
    df.columns = ['USD_INR', 'US_10Y_Yield', 'Nifty_50', 'Brent_Crude']
    
    df = df.ffill().dropna()
    return df


# -----------------------------
# STATIONARITY TRANSFORMATION
# -----------------------------
def make_stationary(df):
    df_transformed = pd.DataFrame(index=df.index)
    transform_map = {}

    for col in df.columns:
        series = df[col]
        pval = adfuller(series)[1]

        if pval > 0.05:
            df_transformed[col] = np.log(series).diff()
            transform_map[col] = "log-diff"
        else:
            df_transformed[col] = series
            transform_map[col] = "level"

    df_transformed = df_transformed.dropna()
    return df_transformed, transform_map


# -----------------------------
# MAIN MODEL
# -----------------------------
def run_var_model(df):
    
    df_t, transform_map = make_stationary(df)

    y = df_t[['USD_INR', 'US_10Y_Yield', 'Nifty_50']]
    exog = df_t[['Brent_Crude']]

    model = VAR(endog=y, exog=exog)
    res = model.fit(maxlags=10, ic='aic')

    # Forecast (constant oil scenario)
    steps = 5
    last_exog = exog.iloc[-1].values
    exog_future = np.tile(last_exog, (steps, 1))

    forecast = res.forecast(
        y.values[-res.k_ar:],
        steps=steps,
        exog_future=exog_future
    )

    forecast_df = pd.DataFrame(
        forecast,
        columns=y.columns
    )

    return res, forecast_df, transform_map


# -----------------------------
# IRF + FEVD
# -----------------------------
def compute_irf(res):
    return res.irf(10)

def compute_fevd(res):
    return res.fevd(10)