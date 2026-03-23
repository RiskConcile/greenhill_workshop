Research the security with ticker $ARGUMENTS. Give me the following:

1. Full name and issuer
2. Investment strategy and asset class
3. Key holdings or market exposure
4. Risk profile — volatility and drawdown characteristics
5. Liquidity — approximate market cap or AUM and daily trading volume
6. Suitability — which investor risk profiles is this appropriate for (Conservative / Moderate / Aggressive)?
7. Verdict — should this be included in a robo-advisor asset universe, and why?

Return the result as a JSON object and append it to data/asset_universe.json.
If the file does not exist, create it as an empty array first, then append the entry.
