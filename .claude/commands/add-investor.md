Create a completely random but realistic investor persona. Be creative — vary the age, background, risk profile, and financial goals each time.

Generate a JSON object with the following fields that matches the submissions.json schema exactly:

- id: a new UUID
- submitted_at: current timestamp in ISO-8601 format
- name: a realistic full name
- investment_horizon: one of "Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "10+ years"
- risk_tolerance: one of "Conservative", "Moderate", "Aggressive"
- liquidity_needs: one of "Low — I won't need this money soon", "Medium — I may need some access", "High — I need regular access"
- return_expectation_pct: an integer between 2 and 20
- constraints: a realistic free-text description of preferences or exclusions

Then append the new investor to data/submissions.json and confirm it was saved.
