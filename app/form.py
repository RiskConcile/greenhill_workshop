import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

SUBMISSIONS_FILE = Path(__file__).parent.parent / "data" / "submissions.json"


def load_submissions():
    if not SUBMISSIONS_FILE.exists():
        return []
    with open(SUBMISSIONS_FILE) as f:
        return json.load(f)


def save_submission(entry):
    submissions = load_submissions()
    submissions.append(entry)
    SUBMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)


st.set_page_config(page_title="Investor Questionnaire", layout="centered")
st.title("Investor Questionnaire")
st.caption("Tell us about your investment goals so we can build a suitable portfolio.")

with st.form("investor_form"):
    name = st.text_input("Full name")

    horizon = st.selectbox(
        "Investment horizon",
        ["Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "10+ years"],
    )

    risk = st.select_slider(
        "Risk tolerance",
        options=["Very low", "Low", "Moderate", "High", "Very high"],
        value="Moderate",
    )

    liquidity = st.selectbox(
        "Liquidity needs",
        [
            "High — may need funds within months",
            "Medium — likely within 1–2 years",
            "Low — no near-term withdrawal expected",
        ],
    )

    return_expectation = st.number_input(
        "Annual return expectation (%)",
        min_value=0.0,
        max_value=50.0,
        value=7.0,
        step=0.5,
        format="%.1f",
    )

    preferences = st.text_area(
        "Preferences or constraints",
        placeholder="e.g. no fossil fuels, prefer index funds, avoid leverage…",
        height=100,
    )

    submitted = st.form_submit_button("Submit", use_container_width=True)

if submitted:
    if not name.strip():
        st.error("Please enter your full name.")
    else:
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "name": name.strip(),
            "investment_horizon": horizon,
            "risk_tolerance": risk,
            "liquidity_needs": liquidity,
            "annual_return_expectation_pct": return_expectation,
            "preferences_or_constraints": preferences.strip(),
        }
        save_submission(entry)
        st.success(f"Submission saved. Reference ID: `{entry['id']}`")
