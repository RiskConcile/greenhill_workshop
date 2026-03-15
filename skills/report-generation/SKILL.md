# Report Generation Skill

## Purpose
Combine all agent outputs into a human-readable portfolio recommendation report.

## When to Use
- After all three agents (intake, market, portfolio) have completed
- When you need to present a final recommendation to the investor
- When generating the rationale text for the Streamlit UI

## Input
1. **Submission** — original form data
2. **Profile** — intake agent output
3. **Market data** — market agent output
4. **Portfolio** — portfolio agent output

## Report Sections

### 1. Investment Profile
A summary paragraph from the intake agent describing the investor.

### 2. Market Conditions
The current market outlook from the market agent.

### 3. Allocation Details
A list of each position with:
- Ticker and name
- Weight as percentage
- Dollar amount (weight * initial_investment)

### 4. Portfolio Characteristics
- Expected Annual Return (percentage)
- Expected Volatility (percentage)
- Risk-Adjusted Score (return / volatility)

### 5. Notes
- Flag if ESG preferences were applied
- Flag if income-generating assets were prioritized
- Restate the risk label and investment horizon

### 6. Disclaimer
Always include: "This is an educational prototype and does NOT constitute financial advice."

## Output
A dict containing:
```json
{
  "investor_name": "Jane Smith",
  "risk_profile": "Moderate",
  "initial_investment": 50000,
  "allocations": [...],
  "expected_return": 0.072,
  "expected_volatility": 0.11,
  "market_conditions": "...",
  "rationale": "### Investment Profile\n..."
}
```

## Implementation
See `agents/master_agent.py` for the reference implementation.