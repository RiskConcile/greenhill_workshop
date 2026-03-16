# Portfolio Construction Skill (LLM-powered)

## Purpose
Use Claude to reason about optimal portfolio allocation — considering
diversification, correlation, risk budgeting, and investor preferences
in ways that a mechanical system cannot.

## Why LLM Instead of Rules?
A rule-based allocator uses fixed tables (e.g., "Moderate = 55% equity").
The LLM can:
- Reason about asset correlation (don't pair two highly correlated ETFs)
- Adjust for current market conditions (overweight bonds in risk-off environments)
- Respect complex constraints from free text ("no energy stocks, prefer healthcare")
- Explain WHY each allocation was chosen (per-asset rationale)
- Balance simplicity vs. diversification (don't create 15-position portfolios)

## When to Use
- After the market agent has returned screened assets
- When you need intelligent, explainable allocation decisions
- When demonstrating LLM reasoning about financial trade-offs

## How It Works
The agent receives:
1. Full investor profile (from intake agent)
2. Screened assets with characteristics (from market agent)
3. Market conditions text

Claude then reasons about the optimal allocation, respecting constraints:
- Weights must sum to 1.0
- Minimum 5% per position
- Maximum 40% per position
- 5-10 positions total

## Output
```json
{
  "allocations": [
    {
      "ticker": "VTI",
      "name": "Vanguard Total Stock Market ETF",
      "asset_class": "US Equity",
      "weight": 0.25,
      "rationale": "Core US equity exposure — largest allocation for growth"
    }
  ],
  "expected_return": 0.072,
  "expected_volatility": 0.11,
  "portfolio_rationale": "Balanced 60/30/10 equity/bond/alt split for moderate risk...",
  "diversification_score": "high"
}
```

## Implementation
See `agents/portfolio_agent.py` — focus on the `SYSTEM_PROMPT` and the
constraint rules embedded in the prompt.