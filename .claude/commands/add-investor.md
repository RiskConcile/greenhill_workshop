Generate a completely random but realistic investor persona and append it to data/submissions.json.

## Instructions

1. Invent a realistic investor persona. Vary the following freely — do not default to similar profiles each time:
   - Age range: anywhere from 22 to 75
   - Background: e.g. software engineer, retired teacher, small business owner, doctor, recent graduate, artist, nurse, lawyer, construction worker, etc.
   - Risk profile: Conservative / Moderate / High / Very high — weighted randomly, not always aggressive
   - Goals: retirement, home purchase, education fund, wealth preservation, income generation, travel, early retirement, etc.
   - Investment horizon: choose from "Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "10+ years"
   - Liquidity needs: choose from "Low — no near-term withdrawal expected", "Medium — may need partial access within 3 years", "High — may need full access within 1 year"
   - Annual return expectation: a realistic number between 3.0 and 20.0 (as a float, in percent)
   - Preferences or constraints: a short natural-language sentence reflecting the persona's actual situation (e.g. ESG preferences, sector avoidance, concentration in real estate, currency needs, etc.)

2. Build a JSON object matching this exact schema:
   - `id`: a new UUID v4 (generate one)
   - `timestamp`: current UTC datetime in ISO 8601 format with timezone offset (e.g. "2026-03-25T14:30:00.000000+00:00")
   - `name`: a realistic full name (first + last), varied in ethnicity and gender
   - `investment_horizon`: string (from the options above)
   - `risk_tolerance`: string — one of: "Conservative", "Moderate", "High", "Very high"
   - `liquidity_needs`: string (from the options above)
   - `annual_return_expectation_pct`: float
   - `preferences_or_constraints`: string

3. Append the new entry to data/submissions.json:
   - Read the file (it exists and contains a JSON array)
   - Append the new object
   - Write the updated array back to data/submissions.json

4. Print a brief summary: the investor's name, risk profile, horizon, and return expectation.
