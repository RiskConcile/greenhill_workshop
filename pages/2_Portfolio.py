import json
from pathlib import Path

import plotly.express as px
import streamlit as st

PORTFOLIOS_PATH = Path(__file__).parent.parent / "data" / "portfolios.json"

if not PORTFOLIOS_PATH.exists():
    PORTFOLIOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PORTFOLIOS_PATH.write_text("[]")

st.set_page_config(page_title="Portfolio", page_icon="📊", layout="centered")
st.title("Portfolio Suggestion")

if not PORTFOLIOS_PATH.exists() or not json.loads(PORTFOLIOS_PATH.read_text()):
    st.info("No portfolios generated yet. Run the pipeline in the Claude Code CLI first.")
    st.stop()

portfolios = json.loads(PORTFOLIOS_PATH.read_text())

names = [p["investor_name"] for p in portfolios]
selected_name = st.selectbox("Select investor", options=names[::-1])
portfolio = next(p for p in reversed(portfolios) if p["investor_name"] == selected_name)

st.subheader(f"{portfolio['investor_name']} — {portfolio['risk_label']} (Risk score: {portfolio['risk_score']}/10)")
st.caption(f"Generated at {portfolio['generated_at']}")

st.divider()

st.markdown("### Narrative")
st.write(portfolio["narrative"])

if portfolio.get("warnings"):
    st.divider()
    st.markdown("### Warnings")
    for w in portfolio["warnings"]:
        st.warning(w)

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Allocation")
    fig = px.pie(
        values=[a["weight_pct"] for a in portfolio["allocation"]],
        names=[a["ticker"] for a in portfolio["allocation"]],
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Asset Class Breakdown")
    summary = portfolio["asset_class_summary"]
    fig2 = px.pie(
        values=list(summary.values()),
        names=list(summary.keys()),
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.markdown("### Positions")
for position in portfolio["allocation"]:
    st.markdown(f"**{position['ticker']}** ({position['asset_class']}) — {position['weight_pct']}%")
    st.caption(position["rationale"])

st.divider()
st.caption(portfolio["disclaimer"])
