"""
Intake Agent (LLM-powered)
===========================
Reads an investor submission and produces a structured risk profile
using Claude to intelligently interpret the investor's full context —
including free-text preferences, inconsistencies between fields, and
nuanced risk signals that rules can't capture.
"""

from .base import call_llm_json

SYSTEM_PROMPT = """\
You are an expert financial intake analyst at a robo-advisor firm.

Your job is to analyze an investor's form submission and produce a structured
risk profile. You must reason holistically — considering how the different
fields interact, not just mapping each field to a number independently.

Key things to consider:
- A "Moderate" risk tolerance with a 20+ year horizon is actually quite
  aggressive in practice — long horizons can tolerate more volatility.
- High liquidity needs reduce effective risk tolerance regardless of stated preference.
- Free-text preferences may reveal important constraints (e.g. "I'm retiring
  next year" in preferences overrides a "10-20 year" horizon selection).
- ESG or sector preferences should be noted and may affect asset selection.
- Income needs shift the portfolio toward dividend/yield-generating assets.

Return your analysis as a JSON object with EXACTLY these keys:
{
  "risk_score": <integer 1-10, where 1=ultra-conservative, 10=ultra-aggressive>,
  "risk_label": "<one of: Conservative, Moderate-Conservative, Moderate, Moderate-Aggressive, Aggressive>",
  "summary": "<2-3 sentence natural language summary of the investor's profile>",
  "reasoning": "<1-2 sentences explaining WHY you chose this risk score>",
  "flags": ["<any warnings or notable observations, e.g. 'stated horizon conflicts with preferences'>"],
  "investment_horizon": "<from the submission>",
  "income_needs": "<from the submission>",
  "preferences": "<from the submission, or empty string>",
  "initial_investment": <number from the submission>,
  "esg_preference": <true or false>,
  "sector_preferences": ["<any sectors mentioned in preferences>"]
}

Return ONLY the JSON object, no other text."""


def analyze_investor_profile(submission: dict, api_key: str | None = None) -> dict:
    """
    Use Claude to analyze an investor submission and return a risk profile.

    Parameters
    ----------
    submission : dict
        Raw form data from the investor intake form.
    api_key : str, optional
        Anthropic API key. Falls back to env var.

    Returns
    -------
    dict — structured risk profile with LLM reasoning.
    """
    user_message = f"""\
Analyze this investor submission and produce a risk profile:

Name: {submission.get('name', 'Unknown')}
Initial Investment: ${submission.get('initial_investment', 0):,.0f}
Investment Horizon: {submission.get('investment_horizon', 'Not specified')}
Risk Tolerance (stated): {submission.get('risk_tolerance', 'Not specified')}
Liquidity Needs: {submission.get('liquidity_needs', 'Not specified')}
Return Expectation: {submission.get('return_expectation', 'Not specified')}
Income Needs: {submission.get('income_needs', 'Not specified')}
Additional Preferences: {submission.get('preferences', 'None')}
"""

    return call_llm_json(SYSTEM_PROMPT, user_message, api_key)