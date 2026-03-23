Run the full robo-advisor pipeline for the investor named "$ARGUMENTS".

Spawn a subagent for each step below and pass the output of each into the next:

1. Intake Subagent — read data/submissions.json, find "$ARGUMENTS", and apply
   the investor-profiler skill in skills/investor-profiler/SKILL.md to produce
   a structured risk profile.

2. Market Subagent — read data/asset_universe.json and apply the asset-screener
   skill in skills/asset-screener/SKILL.md against the risk profile to produce
   a shortlist of suitable assets.

3. Portfolio Subagent — apply the portfolio-constructor skill in
   skills/portfolio-constructor/SKILL.md using the risk profile and the
   screened shortlist to build a final allocation.

4. Using all three outputs, apply the report-writer skill in
   skills/report-writer/SKILL.md to write the final recommendation and
   append it to data/portfolios.json.
