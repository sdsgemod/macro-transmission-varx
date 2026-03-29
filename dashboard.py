import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib.pyplot as plt

from engine import get_macro_data, run_var_model, compute_irf, compute_fevd


# -----------------------------
# BUILD DASHBOARD
# -----------------------------
def build_dashboard():

    df = get_macro_data()
    res, forecast_df, transform_map = run_var_model(df)

    forecast_index = pd.date_range(
        start=df.index[-1],
        periods=6,
        freq='B'
    )[1:]

    forecast_df.index = forecast_index

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # NIFTY
    fig.add_trace(go.Scatter(
        x=df.index[-150:], 
        y=df['Nifty_50'][-150:],
        name="Nifty 50",
        line=dict(width=2)
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=forecast_df.index, 
        y=forecast_df['Nifty_50'],
        name="Nifty Forecast",
        line=dict(dash='dot')
    ), secondary_y=False)

    # USD/INR
    fig.add_trace(go.Scatter(
        x=df.index[-150:], 
        y=df['USD_INR'][-150:],
        name="USD/INR",
        line=dict(dash='dash')
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=forecast_df.index, 
        y=forecast_df['USD_INR'],
        name="USD/INR Forecast",
        line=dict(dash='dot')
    ), secondary_y=True)

    # US10Y
    fig.add_trace(go.Scatter(
        x=df.index[-150:], 
        y=df['US_10Y_Yield'][-150:],
        name="US 10Y Yield",
        line=dict(width=1)
    ), secondary_y=True)

    fig.update_layout(
        title="Macro Transmission Dashboard (VARX Framework)",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig, res


# -----------------------------
# EXPORT FULL HTML REPORT
# -----------------------------
def export_full_report():

    df = get_macro_data()
    fig, res = build_dashboard()

    # Save interactive dashboard
    fig.write_html("Macro_Dashboard.html")

    # IRF & FEVD
    irf = compute_irf(res)
    fevd = compute_fevd(res)

    fig_irf = irf.plot(orth=True)
    plt.savefig("irf.png")
    plt.close()

    fig_fevd = fevd.plot()
    plt.savefig("fevd.png")
    plt.close()

    # SAFE summary formatting
    summary_text = str(res.summary())

    summary_html = "<pre style='font-family: monospace; background:#111; color:#00ffcc; padding:20px; border-radius:8px; overflow-x:auto;'>"
    summary_html += summary_text
    summary_html += "</pre>"

    # FINAL HTML REPORT
    html_content = """
    <html>
    <head>
        <title>Macro Strategy Report</title>
    </head>
    <body style="background-color:#0b0c10; color:white; font-family:Arial; padding:20px;">
    
        <h1>Macro Transmission Model (VARX)</h1>
        
        <h2>Model Summary</h2>
    """ + summary_html + """

        <h2>Impulse Response Functions</h2>
        <img src="irf.png" width="800">

        <h2>Variance Decomposition</h2>
        <img src="fevd.png" width="800">

        <h2>Interactive Dashboard</h2>
        <iframe src="Macro_Dashboard.html" width="100%" height="600"></iframe>

        <p><b>Note:</b> Forecast assumes constant Brent crude (ceteris paribus scenario).</p>

    </body>
    </html>
    """

    with open("Full_Macro_Report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Full report exported: Full_Macro_Report.html")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    export_full_report()