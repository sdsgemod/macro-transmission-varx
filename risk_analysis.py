import plotly.graph_objects as go
import pandas as pd
import numpy as np

from engine import get_macro_data


# -----------------------------
# BUILD RISK DASHBOARD
# -----------------------------
def build_risk_dashboard():

    df = get_macro_data()
    returns = df.pct_change().dropna()

    # Rolling Correlation
    corr = returns['Nifty_50'].rolling(30).corr(returns['USD_INR'])

    # Rolling Beta
    beta = (
        returns['Nifty_50'].rolling(30).cov(returns['USD_INR']) /
        returns['USD_INR'].rolling(30).var()
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=corr.index,
        y=corr,
        name="Rolling Correlation",
        line=dict(width=2)
    ))

    fig.add_trace(go.Scatter(
        x=beta.index,
        y=beta,
        name="Rolling Beta",
        line=dict(width=2, dash='dot')
    ))

    # Regime line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="white"
    )

    fig.update_layout(
        title="Risk Monitor: FX-Equity Transmission",
        template="plotly_dark",
        yaxis=dict(range=[-1.2, 1.2])
    )

    return fig, corr.iloc[-1], beta.iloc[-1]


# -----------------------------
# EXPORT HTML
# -----------------------------
def export_risk_report():

    fig, latest_corr, latest_beta = build_risk_dashboard()

    fig.write_html("Risk_Monitor.html")

    print("\n========== RISK SUMMARY ==========")
    print(f"Latest Correlation: {latest_corr:.2f}")
    print(f"Latest Beta: {latest_beta:.2f}")

    if latest_corr > -0.3:
        print("⚠️ Regime weakening (decoupling risk)")
    else:
        print("✅ Normal EM regime intact")

    print("=================================\n")
    print("✅ Risk dashboard exported: Risk_Monitor.html")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    export_risk_report()