"""
Page 2 — View Submissions
==========================
Browse and inspect all stored investor submissions.
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "submissions.json"


def load_submissions() -> list[dict]:
    """Load existing submissions from JSON file."""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


# ── Page Header ──────────────────────────────────────────────
st.title("Investor Submissions")

submissions = load_submissions()

if not submissions:
    st.info("No submissions yet. Go to the **Investor Form** page to create one.")
    st.stop()

st.markdown(f"**{len(submissions)}** submission(s) on file.")
st.divider()

# ── Summary Table ────────────────────────────────────────────
df = pd.DataFrame(submissions)
display_cols = ["name", "risk_tolerance", "investment_horizon", "initial_investment", "timestamp"]
available_cols = [c for c in display_cols if c in df.columns]
st.dataframe(
    df[available_cols],
    use_container_width=True,
    hide_index=True,
    column_config={
        "initial_investment": st.column_config.NumberColumn("Investment ($)", format="$%d"),
        "timestamp": st.column_config.DatetimeColumn("Submitted At", format="MMM DD, YYYY HH:mm"),
    },
)

# ── Detail View ──────────────────────────────────────────────
st.divider()
st.subheader("Submission Detail")

selected_name = st.selectbox(
    "Select an investor",
    options=[s["name"] for s in submissions],
)

selected = next(s for s in submissions if s["name"] == selected_name)

col1, col2 = st.columns(2)
with col1:
    st.metric("Risk Tolerance", selected["risk_tolerance"])
    st.metric("Horizon", selected["investment_horizon"])
    st.metric("Investment", f"${selected['initial_investment']:,.0f}")
with col2:
    st.metric("Liquidity Needs", selected.get("liquidity_needs", "N/A"))
    st.metric("Return Expectation", selected.get("return_expectation", "N/A"))
    st.metric("Income Needs", selected.get("income_needs", "N/A"))

if selected.get("preferences"):
    st.markdown(f"**Preferences:** {selected['preferences']}")

with st.expander("Raw JSON"):
    st.json(selected)