Run the full LLM-powered robo-advisor pipeline for an investor: $ARGUMENTS

This command orchestrates all four agents in sequence, demonstrating the
**subagent collaboration pattern** from the workshop.

## Steps

1. **Load submission** — Read `data/submissions.json` and find the matching investor
   (by name, partial name, or "latest" for the most recent).

2. **Launch Intake Subagent** — Run `agents/intake_agent.py` to analyze the profile.
   Show the LLM's reasoning about risk score and any flags.

3. **Launch Market Subagent** — Run `agents/market_agent.py` which uses **tool calling**
   to screen the asset universe. Show which tools were invoked and what was filtered.

4. **Launch Portfolio Subagent** — Run `agents/portfolio_agent.py` to construct
   the allocation. Show the per-asset rationale.

5. **Launch Master Orchestrator** — Run `agents/master_agent.py` to synthesize
   everything into a final recommendation with narrative rationale.

Execute this as a Python script:

```python
import json, os
from agents.intake_agent import analyze_investor_profile
from agents.market_agent import gather_market_data
from agents.portfolio_agent import build_portfolio
from agents.master_agent import orchestrate

api_key = os.environ.get("ANTHROPIC_API_KEY")

with open("data/submissions.json") as f:
    subs = json.load(f)

target = subs[-1]  # latest submission
print(f"Running pipeline for: {target['name']}")

print("\n--- STEP 1: Intake Agent ---")
profile = analyze_investor_profile(target, api_key)
print(json.dumps(profile, indent=2))

print("\n--- STEP 2: Market Agent (with tool calls) ---")
market = gather_market_data(profile, api_key)
print(json.dumps(market, indent=2))

print("\n--- STEP 3: Portfolio Agent ---")
portfolio = build_portfolio(profile, market, api_key)
print(json.dumps(portfolio, indent=2))

print("\n--- STEP 4: Master Agent ---")
result = orchestrate(target, profile, market, portfolio, api_key)
print(json.dumps(result, indent=2))
```

After running, present the results in a clear format showing:
- The agent chain: Intake → Market → Portfolio → Master
- How data flows between agents
- Where the LLM added intelligence vs. what rules would have done
- The final portfolio recommendation with rationale

This is the core workshop demonstration of **multi-agent collaboration**.