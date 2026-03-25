Run the full robo-advisor pipeline for the investor named "$ARGUMENTS".

## Instructions

You are the master agent. Run all four steps below in strict sequence, passing each output into the next. Do not skip steps or abort early.

All files are under the project root: the working directory of this Claude Code session.

---

## Step 1 — Intake Agent (investor-profiler skill)

1. Read `data/submissions.json`
2. Find the entry where `name` matches "$ARGUMENTS" (case-insensitive). If no match is found, stop and report: "No submission found for investor: $ARGUMENTS"
3. Read `skills/investor-profiler/SKILL.md`
4. Apply the skill exactly as specified to produce a structured risk profile JSON object
5. Keep this object in memory — it is passed to steps 2, 3, and 4

---

## Step 2 — Market Agent (asset-screener skill)

1. Read `data/assets.json` (this is the full asset universe)
2. Read `skills/asset-screener/SKILL.md`
3. Apply the skill using the risk profile from Step 1 as input
4. Produce the screened shortlist JSON object
5. Keep this object in memory — it is passed to steps 3 and 4

---

## Step 3 — Portfolio Agent (portfolio-constructor skill)

1. Read `skills/portfolio-constructor/SKILL.md`
2. Apply the skill using:
   - The risk profile from Step 1
   - The screened shortlist from Step 2
3. Produce the portfolio allocation JSON object
4. Keep this object in memory — it is passed to step 4

---

## Step 4 — Report Writer (report-writer skill)

1. Read `skills/report-writer/SKILL.md`
2. Apply the skill using all three upstream outputs:
   - Risk profile from Step 1
   - Screened shortlist from Step 2
   - Portfolio allocation from Step 3
3. Construct the final report JSON object with a new UUID v4 for `id` and current UTC datetime for `generated_at`
4. Read `data/portfolios.json` — if the file does not exist, treat it as an empty array `[]`
5. Append the new report and write the full updated array back to `data/portfolios.json`
6. Return the final report JSON object

---

## Output

Print a summary with:
- Investor name, risk label, and risk score
- Number of assets evaluated and number excluded
- Final allocation table (ticker, asset class, weight)
- Asset class summary (equities / fixed income / alternatives)
- All warnings surfaced
- Confirmation that `data/portfolios.json` was written and how many entries it now contains
