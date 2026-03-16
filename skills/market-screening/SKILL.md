# Market Screening Skill (LLM-powered with Tool Use)

## Purpose
Use Claude with **tool calling** to intelligently screen an asset universe.
The agent decides what information it needs and makes tool calls to get it.

## Why Tool Use?
This demonstrates the most powerful agentic pattern: the LLM decides what
tools to call, with what parameters, and how many times. Instead of hardcoded
filtering rules, the agent reasons about what assets to look for.

## When to Use
- After the intake agent has produced a risk profile
- When you need to find suitable assets for a specific investor
- When demonstrating the tool-use / function-calling pattern

## How It Works (Agentic Loop)

The LLM drives the research process using a transparent ETF universe stored
in `data/etf_universe.json` (17 ETFs across 7 categories). Students can open
this file to see exactly what assets are available. Live prices are fetched
from Yahoo Finance via yfinance when available, with silent fallback to
static prices in the JSON file.

```
1. Send investor profile + tool definitions to Claude
2. Claude calls get_market_conditions() to understand the macro environment
3. Claude calls get_available_etfs() to see the full ETF universe
4. Claude optionally calls filter_etfs() to narrow by asset class, volatility, or yield
5. Claude selects 5-8 ETFs and explains why each fits this investor
6. Claude synthesizes all research into final JSON with per-asset rationale
```

This loop runs up to 5 iterations. Claude autonomously decides:
- Which tools to call and in what order
- Whether to filter by specific criteria (e.g., low volatility for conservative investors)
- When it has enough information to stop
- Which assets best fit the investor's risk profile and preferences

## Available Tools

### get_market_conditions
Returns macro environment data: Fed funds rate, 10-year treasury yield,
S&P 500 P/E ratio, inflation, and outlook summaries for equities, bonds,
international markets, and alternatives.

### get_available_etfs
Returns the full list of 17 ETFs from `data/etf_universe.json` with all
metrics: ticker, name, asset class, price (live or static), expense ratio,
dividend yield, 5-year annual return, volatility, and description.

### filter_etfs
Narrows the ETF universe by criteria:
- `asset_class_contains` — substring match (e.g., "Bond", "ESG", "Gold")
- `max_volatility` — only ETFs with volatility <= threshold
- `min_dividend_yield` — only ETFs with yield >= threshold

## Output
```json
{
  "selected_assets": [
    {
      "ticker": "VTI",
      "name": "Vanguard Total Stock Market ETF",
      "asset_class": "US Equity",
      "rationale": "Core US equity exposure — broad market at ultra-low cost"
    }
  ],
  "market_conditions": "Fed paused hikes, inflation moderating. Bond yields attractive...",
  "screening_notes": "Screened for low-volatility bonds and broad equity given moderate risk..."
}
```

## Implementation
See `agents/market_agent.py` — focus on the `TOOLS` definition and the
agentic loop in `gather_market_data()`.