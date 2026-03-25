import json
from pathlib import Path

import plotly.express as px
import streamlit as st

PORTFOLIOS_FILE = Path(__file__).parent.parent.parent / "data" / "portfolios.json"


def load_portfolios():
    if not PORTFOLIOS_FILE.exists():
        PORTFOLIOS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PORTFOLIOS_FILE.write_text("[]")
        return []
    with open(PORTFOLIOS_FILE) as f:
        return json.load(f)


st.set_page_config(page_title="Portfolio Report", layout="wide")
st.title("Portfolio Report")

portfolios = load_portfolios()

if not portfolios:
    st.info("No portfolios have been generated yet. Run the pipeline for an investor first.")
    st.stop()

investor_names = list({p["investor_name"] for p in portfolios})
selected = st.selectbox("Select investor", sorted(investor_names))

investor_portfolios = [p for p in portfolios if p["investor_name"] == selected]
portfolio = sorted(investor_portfolios, key=lambda p: p["generated_at"])[-1]

st.caption(f"Generated at: {portfolio['generated_at']}  |  Risk: **{portfolio['risk_label']}** ({portfolio['risk_score']}/10)")

# Warnings
if portfolio.get("warnings"):
    st.subheader("Warnings")
    for w in portfolio["warnings"]:
        st.warning(w)

# Narrative
st.subheader("Summary")
st.write(portfolio["narrative"])

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Position Allocation")
    tickers = [a["ticker"] for a in portfolio["allocation"]]
    weights = [a["weight_pct"] for a in portfolio["allocation"]]
    fig1 = px.pie(names=tickers, values=weights, hole=0.35)
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    fig1.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Asset Class Breakdown")
    summary = portfolio["asset_class_summary"]
    classes = ["Equities", "Fixed Income", "Alternatives"]
    class_weights = [summary["equities_pct"], summary["fixed_income_pct"], summary["alternatives_pct"]]
    fig2 = px.pie(names=classes, values=class_weights, hole=0.35,
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig2, use_container_width=True)

# Positions table
st.subheader("Positions")
rows = [
    {"Ticker": a["ticker"], "Asset Class": a["asset_class"], "Weight (%)": a["weight_pct"], "Rationale": a["rationale"]}
    for a in portfolio["allocation"]
]
st.dataframe(rows, use_container_width=True, hide_index=True)

# Disclaimer
st.divider()
st.caption(portfolio.get("disclaimer", ""))
