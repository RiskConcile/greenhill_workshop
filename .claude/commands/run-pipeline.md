Run the full robo-advisor pipeline for the investor named "$ARGUMENTS".

You are the master agent. Spawn 4 subagents in strict sequence — each subagent is single-responsibility. Pass the output of each subagent as input to the next. Do not skip steps or abort early.

All files are under the project root: the working directory of this Claude Code session.

---

## Step 1 — Spawn the Intake Agent

Spawn a subagent with the following task:

> You are the intake agent.
> 1. Read `data/submissions.json`
> 2. Find the entry where `name` matches "$ARGUMENTS" (case-insensitive). If no match is found, return: "ERROR: No submission found for investor: $ARGUMENTS" and stop.
> 3. Read `skills/investor-profiler/SKILL.md`
> 4. Apply the skill exactly as specified to the submission
> 5. Return the structured risk profile as a single JSON object with no markdown wrapping

Wait for the subagent to return. If it returns an ERROR, stop the pipeline and report it to the user.

Store the returned JSON as the **risk profile** — it is passed to Steps 2, 3, and 4.

---

## Step 2 — Spawn the Market Agent

Spawn a subagent with the following task, embedding the risk profile JSON from Step 1 directly into the prompt:

> You are the market agent.
> 1. Read `data/assets.json` (this is the full asset universe)
> 2. Read `skills/asset-screener/SKILL.md`
> 3. Apply the skill using the following investor risk profile as input:
>
> [INSERT RISK PROFILE JSON FROM STEP 1]
>
> 4. Return the screened shortlist as a single JSON object with no markdown wrapping

Wait for the subagent to return.

Store the returned JSON as the **screened shortlist** — it is passed to Steps 3 and 4.

---

## Step 3 — Spawn the Portfolio Agent

Spawn a subagent with the following task, embedding both the risk profile and shortlist JSON directly into the prompt:

> You are the portfolio agent.
> 1. Read `skills/portfolio-constructor/SKILL.md`
> 2. Apply the skill using the following inputs:
>
> Investor risk profile:
> [INSERT RISK PROFILE JSON FROM STEP 1]
>
> Screened shortlist:
> [INSERT SHORTLIST JSON FROM STEP 2]
>
> 3. Return the portfolio allocation as a single JSON object with no markdown wrapping

Wait for the subagent to return.

Store the returned JSON as the **portfolio allocation** — it is passed to Step 4.

---

## Step 4 — Spawn the Report Writer Agent

Spawn a subagent with the following task, embedding all three upstream outputs directly into the prompt:

> You are the report writer agent.
> 1. Read `skills/report-writer/SKILL.md`
> 2. Apply the skill using the following inputs:
>
> Investor risk profile:
> [INSERT RISK PROFILE JSON FROM STEP 1]
>
> Screened shortlist:
> [INSERT SHORTLIST JSON FROM STEP 2]
>
> Portfolio allocation:
> [INSERT ALLOCATION JSON FROM STEP 3]
>
> 3. Construct the final report JSON object with a new UUID v4 for `id` and current UTC datetime for `generated_at`
> 4. Read `data/portfolios.json` — if it does not exist, treat it as an empty array `[]`
> 5. Append the new report and write the full updated array back to `data/portfolios.json`
> 6. Return the final report JSON object with no markdown wrapping

Wait for the subagent to return.

---

## Output

Print a summary with:
- Investor name, risk label, and risk score
- Number of assets evaluated and number excluded
- Final allocation table (ticker, asset class, weight)
- Asset class summary (equities / fixed income / alternatives)
- All warnings surfaced
- Confirmation that `data/portfolios.json` was written and how many entries it now contains
