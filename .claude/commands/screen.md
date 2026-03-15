Gather information about the security or ticker symbol: $ARGUMENTS

You are a market research subagent. Use your knowledge to deeply analyze
the requested security. Think step by step:

1. **Identify the security** — What is it? What index or sector does it track?
2. **Fundamental analysis** — Key metrics:
   - Asset class and sub-class
   - Expense ratio (for ETFs/funds)
   - Historical 5-year and 10-year average annual returns
   - Volatility (standard deviation) and max drawdown
   - Dividend yield and distribution frequency
   - AUM (assets under management) for ETFs
3. **Risk assessment** — Rate on a 1-10 scale with reasoning
4. **Correlation context** — How does this asset correlate with:
   - S&P 500 (broad US equity)
   - US Aggregate Bond index
   - Inflation (CPI)
5. **Portfolio fit** — For which investor profiles is this most suitable?
6. **Current considerations** — Any recent developments affecting this security?

Also check if this ticker exists in our asset universe by reading
`agents/market_agent.py` — if it does, show our internal data for comparison.

Format the output with clear headers. This is for educational purposes — not financial advice.

**IMPORTANT:** Launch a subagent to check our codebase for any references to this
ticker in existing submissions or portfolio outputs:
```
grep -r "$ARGUMENTS" data/ --include="*.json" 2>/dev/null
```