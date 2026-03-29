# Macro Transmission Dashboard (VARX Framework)

## Overview
This project builds a cross-asset macro transmission model using a Vector Autoregression with exogenous variables (VARX).

It analyzes relationships between:
- Nifty 50 (Equity Market)
- USD/INR (Foreign Exchange)
- US 10Y Treasury Yield (Global Rates)
- Brent Crude (Exogenous Shock)

## Methodology
- Data sourced using yfinance
- Stationarity enforced using ADF-based transformation
- VAR model with exogenous variable (Brent crude)
- Lag selection via AIC

## Features
- 5-step ahead macro forecasting
- Impulse Response Function (IRF) analysis
- Forecast Error Variance Decomposition (FEVD)
- Rolling correlation and beta risk monitoring
- Interactive dashboards using Plotly

## Outputs
- Full HTML Macro Report
- Interactive Macro Dashboard
- Risk Monitoring Dashboard

## Key Insight
The model captures transmission channels between oil, FX, yields, and equity markets in an emerging market setting.

## How to Run
```bash
python dashboard.py
python risk_analysis.py

## Author

**Shivam Dubey**

- MA Economics | Applied Econometrics  
- Focus: Macro Strategy, Time Series Modeling, Data Analytics  

📧 Email: shivam.sd1998@gmail.com