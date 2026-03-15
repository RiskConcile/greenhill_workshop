"""
Portfolio Agent (LLM-powered)
==============================
Takes the investor profile and screened assets from previous agents,
then uses Claude to reason about optimal allocation weights.

Unlike a rule-based system, the LLM can consider nuanced factors:
- Correlation between asset classes
- Investor-specific constraints from free text
- Market conditions affecting near-term allocation
- Balancing diversification vs. simplicity
"""

import json
from .base import call_llm_json

SYSTEM_PROMPT = """\
You are a portfolio construction agent at a robo-advisor firm.

Given an investor profile and a list of screened assets, construct a
portfolio allocation. You must reason about:

1. **Asset class diversification** — spread across equity, bonds, and alternatives
2. **Risk budget** — the total portfolio volatility should match the investor's risk tolerance
3. **Correlation** — don't over-concentrate in correlated assets
4. **Income needs** — if income is needed, tilt toward higher-yield assets
5. **ESG/Sector preferences** — respect stated preferences
6. **Market conditions** — adjust for the current environment
7. **Simplicity** — don't allocate trivially small amounts (minimum 5% per position)

IMPORTANT RULES:
- All weights MUST sum to exactly 1.0
- Minimum weight per position: 0.05 (5%)
- Maximum weight per position: 0.40 (40%)
- Include 5-10 positions (not more)
- Only use assets from the provided screened list

Return your analysis as a JSON object:
{
  "allocations": [
    {
      "ticker": "VTI",
      "name": "Vanguard Total Stock Market ETF",
      "asset_class": "US Equity",
      "weight": 0.25,
      "rationale": "Core US equity exposure at 25% — provides broad market growth"
    }
  ],
  "expected_return": 0.072,
  "expected_volatility": 0.11,
  "portfolio_rationale": "2-3 sentence explanation of the overall allocation strategy",
  "diversification_score": "low / moderate / high"
}

Return ONLY the JSON object, no other text."""


def build_portfolio(
    profile: dict,
    market_data: dict,
    api_key: str | None = None,
) -> dict:
    """
    Use Claude to construct an optimal portfolio allocation.

    Parameters
    ----------
    profile : dict
        Output from the intake agent.
    market_data : dict
        Output from the market agent (must include 'assets' or 'selected_assets').
    api_key : str, optional
        Anthropic API key.

    Returns
    -------
    dict with allocations, expected_return, expected_volatility, rationale.
    """
    assets = market_data.get("assets", market_data.get("selected_assets", []))
    conditions = market_data.get("market_conditions", "No market data available.")

    # Format the asset list for the prompt
    assets_text = json.dumps(assets, indent=2)

    user_message = f"""\
Construct a portfolio for this investor:

INVESTOR PROFILE:
- Risk Score: {profile.get('risk_score', 5)}/10
- Risk Label: {profile.get('risk_label', 'Moderate')}
- Summary: {profile.get('summary', '')}
- Investment Horizon: {profile.get('investment_horizon', '5-10 years')}
- Income Needs: {profile.get('income_needs', 'No income needed')}
- ESG Preference: {profile.get('esg_preference', False)}
- Sector Preferences: {', '.join(profile.get('sector_preferences', [])) or 'None'}
- Initial Investment: ${profile.get('initial_investment', 50000):,.0f}

MARKET CONDITIONS:
{conditions}

SCREENED ASSETS (select from these only):
{assets_text}

Build an optimal allocation using 5-10 of these assets. Weights must sum to 1.0."""

    result = call_llm_json(SYSTEM_PROMPT, user_message, api_key)

    # Validate and normalize weights
    allocations = result.get("allocations", [])
    if allocations:
        total = sum(a.get("weight", 0) for a in allocations)
        if total > 0 and abs(total - 1.0) > 0.01:
            for a in allocations:
                a["weight"] = round(a["weight"] / total, 4)

    return result