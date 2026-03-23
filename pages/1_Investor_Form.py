import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

SUBMISSIONS_PATH = Path(__file__).parent.parent / "data" / "submissions.json"

if not SUBMISSIONS_PATH.exists():
    SUBMISSIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUBMISSIONS_PATH.write_text("[]")

st.set_page_config(page_title="Investor Form", page_icon="📋", layout="centered")
st.title("Investor Profile")
st.caption("Tell us about your investment goals so we can build a personalized portfolio.")

with st.form("investor_form"):
    name = st.text_input("Full name", placeholder="e.g. Jane Smith")

    st.divider()

    horizon = st.select_slider(
        "Investment horizon",
        options=["Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "10+ years"],
        value="5–10 years",
    )

    risk_tolerance = st.radio(
        "Risk tolerance",
        options=["Conservative", "Moderate", "Aggressive"],
        horizontal=True,
    )

    liquidity = st.radio(
        "Liquidity needs",
        options=["Low — I won't need this money soon", "Medium — I may need some access", "High — I need regular access"],
        index=0,
    )

    return_expectation = st.slider(
        "Annual return expectation (%)",
        min_value=2,
        max_value=20,
        value=8,
        step=1,
    )

    constraints = st.text_area(
        "Preferences or constraints",
        placeholder="e.g. No fossil fuels, prefer US equities, exclude crypto...",
        height=100,
    )

    submitted = st.form_submit_button("Submit Profile", use_container_width=True)

if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    else:
        submission = {
            "id": str(uuid.uuid4()),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "name": name.strip(),
            "investment_horizon": horizon,
            "risk_tolerance": risk_tolerance,
            "liquidity_needs": liquidity,
            "return_expectation_pct": return_expectation,
            "constraints": constraints.strip(),
        }

        data = json.loads(SUBMISSIONS_PATH.read_text())
        data.append(submission)
        SUBMISSIONS_PATH.write_text(json.dumps(data, indent=2))

        st.success(f"Profile submitted for **{name}**.")
        st.json(submission)
