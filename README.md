**Tech Stack:** Python (statsmodels, pandas), Plotly, HTML (output dashboards)
# Macro Transmission Model (VARX Framework)

## Overview
This project builds a cross-asset macro transmission model using a Vector Autoregression with exogenous variables (VARX).

It analyzes relationships between:
- Nifty 50 (Equity Market)
- USD/INR (Foreign Exchange)
- US 10Y Treasury Yield (Global Rates)
- Brent Crude (Exogenous Shock)

## Executive Summary

This project implements a VARX framework to analyze how equity, FX, and interest rates interact in an emerging market context, with oil acting as an external macro shock.

### Key Insights

- **Oil → FX Transmission:** Brent crude shows a strong positive impact on USD/INR, indicating oil-driven currency depreciation pressure  
- **Equity–FX Link:** Movements in USD/INR influence equity markets, reflecting capital flow sensitivity  
- **Global Rates Spillover:** US 10Y yields exhibit lagged transmission effects across both FX and equity markets  
- **Time-Varying Dynamics:** Cross-asset relationships are not stable and evolve over time  

### Risk Signals

- Rolling correlation shows **periodic breakdowns in the traditional equity–currency relationship**  
- Indicates **regime shifts where hedging strategies may fail**

### Limitations

- Linear VAR structure may not capture nonlinear shocks  
- Oil treated as purely exogenous  
- No structural identification (SVAR not implemented)  

👉 See `Executive_Summary.pdf` for detailed analysis

## Methodology
- Data sourced using yfinance
- Stationarity tested using Augmented Dickey-Fuller (ADF) tests
- Non-stationary series transformed using log-differencing
- VAR model with exogenous variable (Brent crude)
- Lag selection via AIC
- Model estimated using statsmodels VAR framework with exogenous variables

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
The model highlights how external shocks (such as oil prices and global interest rates) propagate through emerging market economies, affecting exchange rates and equity markets.

## How to Run
```bash
python dashboard.py
python risk_analysis.py

## Author

**Shivam Dubey**

- MA Economics | Applied Econometrics  

📧 Email: shivam.sd1998@gmail.com
