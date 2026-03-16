# Investor Intake Parsing Skill (LLM-powered)

## Purpose
Use Claude to intelligently analyze investor form submissions and produce
structured risk profiles with nuanced reasoning that goes beyond simple rules.

## Why LLM Instead of Rules?
A rule-based system maps fields to numbers mechanically. The LLM can:
- Detect contradictions (e.g., "aggressive" tolerance but "retiring next year" in preferences)
- Interpret free-text preferences for ESG, sector, and constraint extraction
- Reason about how fields interact (long horizon + moderate tolerance = effectively aggressive)
- Flag unusual or concerning patterns

## When to Use
- A new investor submission arrives and needs to be analyzed
- You need to extract a risk score with reasoning
- You need to understand the investor's full context for downstream agents

## Input
A JSON object from `data/submissions.json` with investor form fields.

## How It Works
The agent sends the full submission to Claude with a detailed system prompt that
instructs it to:
1. Consider all fields holistically (not independently)
2. Reason about interactions between risk tolerance, horizon, and liquidity
3. Parse free-text preferences for ESG, sector, and constraint signals
4. Produce structured JSON with explicit reasoning

## System Prompt Pattern
```
"You are an expert financial intake analyst... Consider how the different
fields interact, not just mapping each field to a number independently..."
```

The key technique: **structured JSON output via prompt engineering** — the system
prompt specifies the exact JSON schema, and `call_llm_json()` parses the response.

## Output
```json
{
  "risk_score": 7,
  "risk_label": "Moderate-Aggressive",
  "summary": "Jane is a moderately aggressive investor with a 20+ year horizon...",
  "reasoning": "Despite stating 'Moderate' risk tolerance, the 20+ year horizon and low liquidity needs support a higher effective risk score.",
  "flags": ["Stated tolerance (Moderate) is lower than effective risk level"],
  "esg_preference": true,
  "sector_preferences": ["technology", "healthcare"]
}
```

## Implementation
See `agents/intake_agent.py` — focus on the `SYSTEM_PROMPT` constant.