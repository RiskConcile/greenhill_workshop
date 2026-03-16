"""
Robo-Advisor Workshop — Main Entry Point
=========================================
A simple LLM-powered robo-advisor prototype for educational purposes.
Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Robo-Advisor Workshop",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── API Key Management (sidebar) ────────────────────────────
st.sidebar.title("Settings")

api_key = st.sidebar.text_input(
    "Anthropic API Key",
    type="password",
    placeholder="sk-ant-...",
    help="Required for AI-powered portfolio generation. Get one at console.anthropic.com",
)
if api_key:
    st.session_state["api_key"] = api_key
    st.sidebar.success("API key set")
elif "api_key" not in st.session_state:
    st.sidebar.warning("Enter your API key to enable AI features")

st.sidebar.divider()

# ── Quick stats ──────────────────────────────────────────────
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "submissions.json"
if DATA_FILE.exists():
    submissions = json.loads(DATA_FILE.read_text())
    st.sidebar.metric("Total Submissions", len(submissions))
else:
    st.sidebar.metric("Total Submissions", 0)

# ── Main Page ────────────────────────────────────────────────
st.title("Robo-Advisor Workshop")
st.markdown("### Greenhill Capital — AI-Powered Portfolio Advisor")

st.markdown("""
This application demonstrates how **LLM-powered agents** can be applied
to financial use cases. Each agent uses Claude to reason intelligently
about the investor's needs.

Navigate using the sidebar:

1. **Investor Form** — Submit your investment preferences
2. **View Submissions** — Browse all stored investor profiles
3. **Portfolio Suggestion** — Generate an AI-driven portfolio recommendation

---

**How the agent pipeline works:**

The system chains four specialized LLM agents:

| Agent | What it does | How it uses Claude |
|---|---|---|
| **Intake Agent** | Analyzes investor profile | Interprets free-text preferences, flags inconsistencies |
| **Market Agent** | Screens asset universe | Uses **tool calling** to query asset database, reads market conditions |
| **Portfolio Agent** | Constructs allocation | Reasons about diversification, correlation, risk budgeting |
| **Master Agent** | Synthesizes recommendation | Reviews all outputs, writes coherent narrative for investor |

Each agent makes real API calls to Claude — there are no hardcoded rules.
The agents can handle nuanced situations that rule-based systems miss.

---

*This is an educational prototype — not financial advice.*
""")