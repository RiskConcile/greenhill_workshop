"""
Page 3 — Portfolio Suggestion (LLM-powered)
=============================================
Runs the 4-agent LLM pipeline to generate a portfolio recommendation.
Each step makes real Claude API calls.
"""

import streamlit as st
import json
import time
from pathlib import Path

# Import agents
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.intake_agent import analyze_investor_profile
from agents.market_agent import gather_market_data
from agents.portfolio_agent import build_portfolio
from agents.master_agent import orchestrate

DATA_FILE = Path(__file__).parent.parent / "data" / "submissions.json"


def load_submissions() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


# ── Page Header ──────────────────────────────────────────────
st.title("Portfolio Suggestion")
st.caption("Each step below makes a real LLM call to Claude via the Anthropic API.")

# Check for API key
api_key = st.session_state.get("api_key", "")
if not api_key:
    st.warning(
        "Please enter your **Anthropic API key** in the sidebar to use AI-powered "
        "portfolio generation."
    )
    st.stop()

submissions = load_submissions()
if not submissions:
    st.info("No submissions yet. Go to the **Investor Form** page to create one.")
    st.stop()

# ── Select Investor ──────────────────────────────────────────
selected_name = st.selectbox(
    "Select an investor to generate a portfolio for",
    options=[s["name"] for s in submissions],
)
selected = next(s for s in submissions if s["name"] == selected_name)

# Show selected profile
with st.expander("View submission data"):
    st.json(selected)

st.divider()

# ── Run Agent Pipeline ───────────────────────────────────────
if st.button("Generate Portfolio Suggestion", type="primary", use_container_width=True):

    start_time = time.time()

    # ── STEP 1: Intake Agent ─────────────────────────────────
    with st.status("🧠 Intake Agent — Analyzing investor profile...", expanded=True) as status:
        try:
            profile = analyze_investor_profile(selected, api_key)
            st.markdown(f"**Risk Score:** {profile.get('risk_score', '?')}/10 ({profile.get('risk_label', '?')})")
            st.markdown(f"**Summary:** {profile.get('summary', 'N/A')}")
            if profile.get("reasoning"):
                st.markdown(f"**Reasoning:** {profile['reasoning']}")
            if profile.get("flags"):
                for flag in profile["flags"]:
                    st.warning(f"Flag: {flag}")
            status.update(label="Intake Agent complete", state="complete")
        except Exception as e:
            status.update(label="Intake Agent failed", state="error")
            st.error(f"Intake Agent error: {e}")
            st.stop()

    # ── STEP 2: Market Agent (with tool use) ─────────────────
    with st.status("📊 Market Agent — Screening assets with tool calls...", expanded=True) as status:
        try:
            market_data = gather_market_data(profile, api_key)
            assets = market_data.get("assets", market_data.get("selected_assets", []))
            st.markdown(f"**Assets screened:** {len(assets)}")
            st.markdown(f"**Market conditions:** {market_data.get('market_conditions', 'N/A')}")
            if market_data.get("screening_notes"):
                st.markdown(f"**Screening approach:** {market_data['screening_notes']}")
            for asset in assets[:6]:
                rationale = asset.get("rationale", asset.get("asset_class", ""))
                st.markdown(f"  - **{asset['ticker']}** ({asset['name']}): {rationale}")
            if len(assets) > 6:
                st.caption(f"  ... and {len(assets) - 6} more")
            status.update(label="Market Agent complete", state="complete")
        except Exception as e:
            status.update(label="Market Agent failed", state="error")
            st.error(f"Market Agent error: {e}")
            st.stop()

    # ── STEP 3: Portfolio Agent ──────────────────────────────
    with st.status("📐 Portfolio Agent — Constructing optimal allocation...", expanded=True) as status:
        try:
            portfolio = build_portfolio(profile, market_data, api_key)
            allocs = portfolio.get("allocations", [])
            st.markdown(f"**Positions:** {len(allocs)}")
            st.markdown(f"**Expected return:** {portfolio.get('expected_return', 0):.1%}")
            st.markdown(f"**Expected volatility:** {portfolio.get('expected_volatility', 0):.1%}")
            if portfolio.get("portfolio_rationale"):
                st.markdown(f"**Strategy:** {portfolio['portfolio_rationale']}")
            status.update(label="Portfolio Agent complete", state="complete")
        except Exception as e:
            status.update(label="Portfolio Agent failed", state="error")
            st.error(f"Portfolio Agent error: {e}")
            st.stop()

    # ── STEP 4: Master Agent ─────────────────────────────────
    with st.status("🎯 Master Agent — Synthesizing final recommendation...", expanded=True) as status:
        try:
            result = orchestrate(selected, profile, market_data, portfolio, api_key)
            status.update(label="Master Agent complete", state="complete")
        except Exception as e:
            status.update(label="Master Agent failed", state="error")
            st.error(f"Master Agent error: {e}")
            st.stop()

    elapsed = time.time() - start_time
    st.success(f"Pipeline complete in {elapsed:.1f}s — 4 LLM calls made")
    st.divider()

    # ── Display Results ──────────────────────────────────────
    st.subheader("Portfolio Recommendation")
    col1, col2, col3 = st.columns(3)
    col1.metric("Investor", result.get("investor_name", "?"))
    col2.metric("Risk Profile", result.get("risk_profile", "?"))
    col3.metric("Investment", f"${result.get('initial_investment', 0):,.0f}")

    if result.get("confidence"):
        st.caption(f"Confidence: {result['confidence']}")

    if result.get("warnings"):
        for w in result["warnings"]:
            st.warning(w)

    st.divider()

    # Allocation chart
    allocations = result.get("allocations", [])
    if allocations:
        import pandas as pd
        import plotly.express as px

        alloc_df = pd.DataFrame(allocations)
        fig = px.pie(
            alloc_df,
            values="weight",
            names="ticker",
            title="Suggested Portfolio Allocation",
            hole=0.4,
        )
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig, use_container_width=True)

        # Allocation details table
        display_cols = ["ticker", "name", "asset_class", "weight"]
        if "rationale" in alloc_df.columns:
            display_cols.append("rationale")
        st.dataframe(
            alloc_df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "weight": st.column_config.ProgressColumn(
                    "Weight", min_value=0, max_value=1, format="%.0%%"
                ),
            },
        )

    # Rationale narrative
    st.subheader("Investment Rationale")
    st.markdown(result.get("rationale", "No rationale generated."))

    # Agent trace (for learning)
    with st.expander("View full agent trace (for learning)"):
        st.subheader("1. Intake Agent Output")
        st.json(profile)
        st.subheader("2. Market Agent Output")
        st.json(market_data)
        st.subheader("3. Portfolio Agent Output")
        st.json(portfolio)
        st.subheader("4. Master Agent Output")
        st.json(result)

    # Disclaimer
    st.divider()
    st.caption(
        "This is an educational prototype and does NOT constitute financial advice. "
        "Always consult a qualified financial advisor before making investment decisions."
    )