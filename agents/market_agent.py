"""
Market Agent (LLM-powered with Tool Use)
==========================================
Uses Claude to research and select ETFs for an investor profile.

The available ETFs are loaded from `data/etf_universe.json` — a small,
transparent file that students can open and inspect. This keeps the
workshop focused on learning LLM concepts (tool use, agentic loops)
rather than hiding assets in code.

The agent demonstrates the TOOL USE pattern:
  - Claude receives tools but decides WHEN and HOW to call them
  - The agentic loop lets Claude make multiple tool calls before responding
  - Claude reasons about which assets fit, rather than applying fixed rules

In production, `get_market_conditions` would call a real market data API
and `get_available_etfs` would query a brokerage or database.
"""

import json
import re
from pathlib import Path
from .base import get_client, DEFAULT_MODEL, MAX_TOKENS


# ── Load ETF Universe from file ─────────────────────────────
# Students can open data/etf_universe.json to see exactly what's available.
_DATA_DIR = Path(__file__).parent.parent / "data"

# Cache for live prices (fetched once per session)
_live_prices: dict[str, float] = {}
_prices_fetched: bool = False


def _fetch_live_prices(tickers: list[str]) -> dict[str, float]:
    """
    Fetch live prices from Yahoo Finance via yfinance.

    Returns a dict of {ticker: price}. If yfinance is unavailable
    or a ticker fails, that ticker is simply omitted (the caller
    falls back to the static price in etf_universe.json).
    """
    global _live_prices, _prices_fetched

    if _prices_fetched:
        return _live_prices

    try:
        import yfinance as yf
        import logging
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)

        # Download all tickers at once (faster than one-by-one)
        data = yf.download(tickers, period="1d", progress=False, ignore_tz=True)

        if "Close" in data.columns:
            # Multiple tickers → columns are ticker symbols
            for ticker in tickers:
                try:
                    price = float(data["Close"][ticker].dropna().iloc[-1])
                    _live_prices[ticker] = round(price, 2)
                except (KeyError, IndexError):
                    pass  # fallback to static price
        elif not data.empty:
            # Single ticker → no multi-level columns
            try:
                price = float(data["Close"].dropna().iloc[-1])
                _live_prices[tickers[0]] = round(price, 2)
            except (KeyError, IndexError):
                pass

    except ImportError:
        pass  # yfinance not installed — use static prices
    except Exception:
        pass  # network error, API issue, etc. — use static prices

    _prices_fetched = True
    return _live_prices


def _load_etf_universe() -> list[dict]:
    """
    Load ETFs from data/etf_universe.json, enriched with live prices
    from Yahoo Finance when available. Falls back to static prices
    in the JSON if yfinance is unavailable or fails.
    """
    path = _DATA_DIR / "etf_universe.json"
    if not path.exists():
        return []

    universe = json.loads(path.read_text())

    # Try to fetch live prices
    tickers = [etf["ticker"] for etf in universe]
    live = _fetch_live_prices(tickers)

    if live:
        for etf in universe:
            if etf["ticker"] in live:
                etf["price"] = live[etf["ticker"]]
                etf["price_source"] = "live (Yahoo Finance)"
            else:
                etf["price_source"] = "static (from etf_universe.json)"
    else:
        for etf in universe:
            etf["price_source"] = "static (from etf_universe.json)"

    return universe


# ── Tool Definitions ─────────────────────────────────────────
# These are the tools Claude can call. Each one is a function the LLM
# can invoke during its reasoning process.

TOOLS = [
    {
        "name": "get_market_conditions",
        "description": (
            "Fetch current market conditions and economic indicators. "
            "Returns interest rates, equity outlook, bond outlook, and "
            "inflation trends. Call this FIRST to understand the macro "
            "environment before selecting assets."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_available_etfs",
        "description": (
            "Get the full list of ETFs available in our universe. "
            "Returns all ETFs with their key metrics: asset class, "
            "expense ratio, yield, historical return, and volatility. "
            "You MUST select only from this list."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "filter_etfs",
        "description": (
            "Filter the ETF universe by criteria. Use this to narrow "
            "down candidates for specific asset classes or characteristics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "asset_class_contains": {
                    "type": "string",
                    "description": (
                        "Filter by asset class (substring match, case-insensitive). "
                        "E.g. 'Equity', 'Bond', 'ESG', 'Gold', 'Real Estate'"
                    ),
                },
                "max_volatility": {
                    "type": "number",
                    "description": "Only return ETFs with volatility <= this value",
                },
                "min_dividend_yield": {
                    "type": "number",
                    "description": "Only return ETFs with dividend yield >= this value",
                },
            },
            "required": [],
        },
    },
]


# ── Simulated market conditions ──────────────────────────────
# In production this would call a real market data API.

_MARKET_CONDITIONS = {
    "date": "2026-03-15 (simulated for workshop)",
    "fed_funds_rate": "4.50%",
    "ten_year_treasury": "4.20%",
    "sp500_pe_ratio": 21.2,
    "inflation_yoy": "2.5%",
    "summary": (
        "Markets are moderately constructive. The Fed has paused rate hikes. "
        "Inflation is moderating toward target. Equity valuations are near "
        "historical averages. Bond yields remain attractive after the hiking cycle."
    ),
    "equity_outlook": "Neutral to slightly bullish. Solid earnings growth but valuations are not cheap.",
    "bond_outlook": "Attractive yields. Duration risk moderate with rates potentially peaking.",
    "international_outlook": "Developed markets at ~30% discount to US. Emerging markets mixed.",
    "alternatives_outlook": "Gold strong on geopolitical uncertainty. Real estate under pressure from rates.",
}


def _execute_tool(name: str, inputs: dict) -> str:
    """Execute a tool call and return the result as a string."""

    if name == "get_market_conditions":
        return json.dumps(_MARKET_CONDITIONS, indent=2)

    elif name == "get_available_etfs":
        universe = _load_etf_universe()
        return json.dumps(universe, indent=2)

    elif name == "filter_etfs":
        universe = _load_etf_universe()
        results = universe

        if inputs.get("asset_class_contains"):
            filt = inputs["asset_class_contains"].lower()
            results = [e for e in results if filt in e.get("asset_class", "").lower()]

        if inputs.get("max_volatility"):
            results = [e for e in results if e.get("volatility", 99) <= inputs["max_volatility"]]

        if inputs.get("min_dividend_yield"):
            results = [e for e in results if e.get("dividend_yield", 0) >= inputs["min_dividend_yield"]]

        return json.dumps(results, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


SYSTEM_PROMPT = """\
You are a market research agent at a robo-advisor firm.

Given an investor's risk profile, your job is to select the best ETFs
from our available universe. You have access to three tools:

1. **get_market_conditions** — Check the current macro environment first
2. **get_available_etfs** — See the full list of ETFs we offer
3. **filter_etfs** — Narrow the list by asset class, volatility, or yield

Your workflow:
1. Call get_market_conditions to understand the environment
2. Call get_available_etfs to see what's available
3. Optionally call filter_etfs to focus on specific categories
4. Select the best 5-8 ETFs for this investor and explain why

You MUST only recommend ETFs from the available universe. Think carefully
about which assets suit this investor's risk level, horizon, income needs,
and any stated preferences (ESG, sector, etc.).

After researching, respond with a JSON object:
{
  "selected_assets": [
    {
      "ticker": "VTI",
      "name": "Vanguard Total Stock Market ETF",
      "asset_class": "US Equity",
      "rationale": "Why this ETF fits this specific investor"
    }
  ],
  "market_conditions": "2-3 sentence summary relevant to this investor",
  "screening_notes": "What you looked for and why"
}

Return ONLY the JSON — no extra text."""


def gather_market_data(profile: dict, api_key: str | None = None) -> dict:
    """
    Use Claude with tool calls to research and select suitable ETFs.

    This runs a multi-turn agentic loop:
      1. Send the investor profile to Claude with tools available
      2. Claude calls tools (market conditions, ETF list, filters)
      3. We execute the tools and return results
      4. Claude makes more tool calls or produces a final answer
      5. Repeat until Claude stops calling tools (up to 5 iterations)

    Parameters
    ----------
    profile : dict
        Output from the intake agent.
    api_key : str, optional
        Anthropic API key.

    Returns
    -------
    dict with selected_assets, market_conditions, screening_notes
    """
    client = get_client(api_key)

    user_message = f"""\
Research and select suitable ETFs for this investor:

Risk Score: {profile.get('risk_score', 5)}/10
Risk Label: {profile.get('risk_label', 'Moderate')}
Profile Summary: {profile.get('summary', 'No summary')}
Reasoning: {profile.get('reasoning', '')}
Investment Horizon: {profile.get('investment_horizon', '5-10 years')}
Income Needs: {profile.get('income_needs', 'No income needed')}
ESG Preference: {profile.get('esg_preference', False)}
Sector Preferences: {', '.join(profile.get('sector_preferences', [])) or 'None'}
Flags: {', '.join(profile.get('flags', [])) or 'None'}
Initial Investment: ${profile.get('initial_investment', 50000):,.0f}

Check market conditions, review our ETF universe, and select 5-8 ETFs
that would form a well-diversified portfolio for this investor."""

    messages = [{"role": "user", "content": user_message}]

    # ── Agentic tool-use loop ────────────────────────────────
    # Claude decides what tools to call and when to stop.
    # We cap at 5 iterations to prevent runaway loops.
    for _ in range(5):
        response = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=0.2,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        tool_calls = [b for b in response.content if b.type == "tool_use"]

        if not tool_calls:
            # Claude is done — extract the final text
            text = "".join(b.text for b in response.content if b.type == "text")
            break

        # Execute each tool and send results back to Claude
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tc in tool_calls:
            result = _execute_tool(tc.name, tc.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result,
            })
        messages.append({"role": "user", "content": tool_results})

    else:
        # Reached max iterations — use whatever text we have
        text = "".join(b.text for b in response.content if b.type == "text")

    # ── Parse the JSON response ──────────────────────────────
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    json_str = fence_match.group(1).strip() if fence_match else text.strip()

    try:
        result = json.loads(json_str)
    except json.JSONDecodeError:
        brace_match = re.search(r"\{.*\}", json_str, re.DOTALL)
        if brace_match:
            result = json.loads(brace_match.group())
        else:
            result = {
                "selected_assets": [],
                "market_conditions": text[:500],
                "screening_notes": "Could not parse LLM response.",
            }

    # Normalize key names for downstream compatibility
    if "selected_assets" in result and "assets" not in result:
        result["assets"] = result["selected_assets"]

    return result