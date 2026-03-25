Research the ETF with ticker $ARGUMENTS using web search and return a structured JSON object.

Gather the following:

1. Full name and issuer
2. Investment strategy and asset class (include expense ratio if available)
3. Key holdings or market exposure — top holdings, sector weights, number of holdings
4. Risk profile — beta (vs S&P 500), annualized standard deviation, 1-year max drawdown, max drawdown since inception, and any notes on concentration or factor risk
5. Liquidity — AUM in USD, average daily trading volume, and any notes on bid-ask spreads or trading characteristics
6. Suitability — which investor risk profiles is this ETF appropriate for? Choose from: Conservative, Moderate, Aggressive
7. Verdict — should this be included in a robo-advisor asset universe, and why? (1–2 sentences)

Structure the result as a JSON object with these exact fields:
- ticker
- full_name
- investment_strategy (string)
- key_holdings (object or string)
- risk_profile (object: beta, annualized_standard_deviation, max_drawdown_1yr, max_drawdown_since_inception, notes)
- liquidity (object: aum_usd, avg_daily_volume, notes)
- suitability (array of strings)
- verdict (string)

Once you have the JSON object, append it to data/assets.json:
- Read the file if it exists; if it does not exist, start with an empty array
- Append the new entry to the array
- Write the updated array back to data/assets.json

Confirm when done by printing the ticker and the updated count of entries in data/assets.json.
