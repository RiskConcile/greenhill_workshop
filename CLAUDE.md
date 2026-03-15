# Robo-Advisor Workshop Project

## Project Overview
An LLM-powered robo-advisor prototype built with **Python + Streamlit + Anthropic SDK**.
Each agent in the pipeline makes real Claude API calls to reason about investor profiles,
screen assets, construct portfolios, and generate recommendations.

This is NOT a rule-based system — every agent uses Claude to make intelligent decisions.

## Tech Stack
- **Frontend/Backend**: Streamlit (Python)
- **AI/LLM**: Anthropic Python SDK (Claude claude-sonnet-4-20250514)
- **Storage**: JSON file (`data/submissions.json`)
- **Language**: Python 3.10+

## Project Structure
```
robo-advisor-workshop/
├── app.py                          # Main Streamlit entry point (API key management)
├── pages/
│   ├── 1_Investor_Form.py          # Intake form (stores to JSON)
│   ├── 2_View_Submissions.py       # Browse stored submissions
│   └── 3_Portfolio_Suggestion.py   # Runs 4-agent LLM pipeline
├── data/
│   └── submissions.json            # Stored investor submissions
├── agents/
│   ├── base.py                     # Shared: Anthropic client, call_llm, call_llm_json, call_llm_with_tools
│   ├── intake_agent.py             # LLM agent: analyzes risk profile from submission
│   ├── market_agent.py             # LLM agent: uses TOOL CALLING to screen assets
│   ├── portfolio_agent.py          # LLM agent: constructs allocation with reasoning
│   └── master_agent.py             # LLM agent: synthesizes final recommendation
├── .claude/commands/               # Slash commands for Claude Code
│   ├── screen.md                   # /screen <ticker> — research a security
│   ├── profile-risk.md             # /profile-risk <name> — analyze an investor
│   ├── compare-assets.md           # /compare-assets <tickers> — compare securities
│   └── run-pipeline.md             # /run-pipeline <name> — run full agent chain
├── skills/                         # Reusable skill definitions
│   ├── investor-intake/SKILL.md
│   ├── market-screening/SKILL.md
│   ├── portfolio-construction/SKILL.md
│   └── report-generation/SKILL.md
├── requirements.txt
└── CLAUDE.md                       # This file
```

## Agent Architecture

The system uses a **4-agent pipeline** where each agent is an LLM call:

```
Investor Form → [Intake Agent] → [Market Agent] → [Portfolio Agent] → [Master Agent] → Recommendation
                  (structured      (tool calling     (allocation        (synthesis &
                   output)          to screen DB)     reasoning)         narrative)
```

### Key Patterns Demonstrated:
1. **Structured JSON output** — Intake Agent returns typed JSON via prompt engineering
2. **Tool use / function calling** — Market Agent uses tools to query the asset database
3. **Multi-turn agentic loop** — Market Agent makes multiple tool calls before responding
4. **Chain-of-agents** — Each agent's output feeds into the next
5. **Synthesis agent** — Master Agent reviews all outputs and produces coherent narrative

## API Key
The Anthropic API key can be provided via:
1. The Streamlit sidebar text input
2. `ANTHROPIC_API_KEY` environment variable

## Coding Conventions
- Use type hints on all function signatures
- Each agent has a SYSTEM_PROMPT constant defining its behavior
- Agent functions accept an optional `api_key` parameter
- Use `call_llm_json()` for structured output, `call_llm()` for free text
- Use `call_llm_with_tools()` for tool-calling agents
- Keep agent system prompts detailed — they ARE the logic
- Store data as JSON with ISO-8601 timestamps

## Key Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run the app
streamlit run app.py

# Run pipeline from command line
python -c "
from agents.intake_agent import analyze_investor_profile
from agents.market_agent import gather_market_data
from agents.portfolio_agent import build_portfolio
from agents.master_agent import orchestrate
import json

with open('data/submissions.json') as f:
    sub = json.load(f)[-1]

profile = analyze_investor_profile(sub)
market = gather_market_data(profile)
portfolio = build_portfolio(profile, market)
result = orchestrate(sub, profile, market, portfolio)
print(json.dumps(result, indent=2))
"
```

## Important Notes
- This is an educational prototype, NOT financial advice
- Each "Generate Portfolio" click makes 4 API calls to Claude
- The Market Agent's tool calls are against a simulated asset database
- Agent prompts are in the SYSTEM_PROMPT constants — editing them changes behavior