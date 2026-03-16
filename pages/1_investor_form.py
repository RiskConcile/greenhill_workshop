"""
Page 1 — Investor Intake Form
===============================
Collects investor preferences and stores them as JSON.
"""

import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "submissions.json"


def load_submissions() -> list[dict]:
    """Load existing submissions from JSON file."""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_submission(submission: dict) -> None:
    """Append a new submission to the JSON file."""
    submissions = load_submissions()
    submissions.append(submission)
    DATA_FILE.write_text(json.dumps(submissions, indent=2))


# ── Page Header ──────────────────────────────────────────────
st.title("Investor Intake Form")
st.markdown("Fill out your investment preferences below. All fields are required.")
st.divider()

# ── Form ─────────────────────────────────────────────────────
with st.form("investor_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Full Name",
            placeholder="e.g. Jane Smith",
        )
        email = st.text_input(
            "Email Address",
            placeholder="e.g. jane@example.com",
        )
        initial_investment = st.number_input(
            "Initial Investment ($)",
            min_value=1_000,
            max_value=10_000_000,
            value=50_000,
            step=5_000,
        )
        investment_horizon = st.select_slider(
            "Investment Horizon",
            options=[
                "< 1 year",
                "1-3 years",
                "3-5 years",
                "5-10 years",
                "10-20 years",
                "20+ years",
            ],
            value="5-10 years",
        )

    with col2:
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
            index=2,
        )
        liquidity_needs = st.selectbox(
            "Liquidity Needs",
            options=["High — may need funds within months",
                     "Medium — may need funds within 1-2 years",
                     "Low — funds can stay invested long-term"],
            index=2,
        )
        return_expectation = st.selectbox(
            "Annual Return Expectation",
            options=["2-4% (capital preservation)",
                     "4-6% (income focus)",
                     "6-8% (balanced growth)",
                     "8-12% (growth focus)",
                     "12%+ (aggressive growth)"],
            index=2,
        )
        income_needs = st.selectbox(
            "Income Needs",
            options=["No income needed",
                     "Some income preferred",
                     "Regular income required"],
            index=0,
        )

    st.divider()

    preferences = st.text_area(
        "Additional Preferences or Constraints",
        placeholder="e.g. ESG focus, no tobacco or firearms, prefer US equities, interested in tech sector...",
        height=100,
    )

    submitted = st.form_submit_button("Submit", type="primary", use_container_width=True)

# ── Handle Submission ────────────────────────────────────────
if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    elif not email.strip():
        st.error("Please enter your email address.")
    else:
        submission = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "name": name.strip(),
            "email": email.strip(),
            "initial_investment": initial_investment,
            "investment_horizon": investment_horizon,
            "risk_tolerance": risk_tolerance,
            "liquidity_needs": liquidity_needs,
            "return_expectation": return_expectation,
            "income_needs": income_needs,
            "preferences": preferences.strip(),
        }
        save_submission(submission)
        st.success(f"Submission saved for **{name}** (ID: `{submission['id'][:8]}...`)")
        st.balloons()