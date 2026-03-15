"""
Master Agent (LLM-powered Orchestrator)
=========================================
Coordinates the full pipeline and generates a final, human-readable
investment recommendation by synthesizing all agent outputs through
a final LLM call.

This is the "brain" that ties everything together — it doesn't just
concatenate outputs, it reasons about the full picture and produces
a coherent narrative.
"""

from .base import call_llm_json
import json

SYSTEM_PROMPT = """\
You are the master orchestrator agent at a robo-advisor firm. You receive
the outputs from three specialized agents:

1. **Intake Agent** — analyzed the investor's profile and risk tolerance
2. **Market Agent** — screened the asset universe and assessed market conditions
3. **Portfolio Agent** — constructed an allocation with weights and rationale

Your job is to:
- Review all three outputs for consistency and quality
- Generate a final, polished recommendation narrative
- Flag any concerns (e.g. portfolio doesn't match risk profile)
- Produce a clear, actionable summary the investor can understand

Return a JSON object:
{
  "investor_name": "...",
  "risk_profile": "...",
  "initial_investment": 50000,
  "allocations": [
    {"ticker": "VTI", "name": "...", "asset_class": "...", "weight": 0.25, "rationale": "..."}
  ],
  "expected_return": 0.072,
  "expected_volatility": 0.11,
  "market_conditions": "...",
  "rationale": "A multi-paragraph markdown narrative covering: investor profile, market context, allocation logic, risk considerations, and any caveats.",
  "confidence": "low / moderate / high",
  "warnings": ["any issues or concerns about the recommendation"]
}

The 'rationale' field should be a well-structured markdown narrative with
### headers for each section. Write it as if you're explaining the
recommendation to the investor directly.

Return ONLY the JSON object."""


def orchestrate(
    submission: dict,
    profile: dict,
    market_data: dict,
    portfolio: dict,
    api_key: str | None = None,
) -> dict:
    """
    Final LLM-powered orchestration: synthesize all agent outputs
    into a polished recommendation.

    Parameters
    ----------
    submission : dict  — Original investor form data.
    profile : dict     — Intake agent output.
    market_data : dict — Market agent output.
    portfolio : dict   — Portfolio agent output.
    api_key : str      — Anthropic API key.

    Returns
    -------
    dict — Final recommendation with narrative rationale.
    """
    user_message = f"""\
Review these agent outputs and produce a final investment recommendation:

═══ ORIGINAL SUBMISSION ═══
{json.dumps(submission, indent=2)}

═══ INTAKE AGENT OUTPUT ═══
{json.dumps(profile, indent=2)}

═══ MARKET AGENT OUTPUT ═══
{json.dumps(market_data, indent=2)}

═══ PORTFOLIO AGENT OUTPUT ═══
{json.dumps(portfolio, indent=2)}

Synthesize these into a final recommendation. Check for consistency between
the risk profile and the proposed allocation. Write the rationale as a clear
narrative the investor can understand."""

    result = call_llm_json(SYSTEM_PROMPT, user_message, api_key)

    # Ensure required fields exist with sensible defaults
    result.setdefault("investor_name", submission.get("name", "Unknown"))
    result.setdefault("risk_profile", profile.get("risk_label", "Moderate"))
    result.setdefault("initial_investment", submission.get("initial_investment", 50_000))
    result.setdefault("allocations", portfolio.get("allocations", []))
    result.setdefault("expected_return", portfolio.get("expected_return", 0))
    result.setdefault("expected_volatility", portfolio.get("expected_volatility", 0))
    result.setdefault("market_conditions", market_data.get("market_conditions", ""))
    result.setdefault("rationale", "No rationale generated.")

    return result