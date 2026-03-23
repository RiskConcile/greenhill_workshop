# Workshop Script — Prompt-by-Prompt Guide

> Start with only `README.md` in the repository.
> Every prompt below is typed directly into the Claude Code CLI.

---

## Stage 1 — Generate CLAUDE.md

> Show students the README. Explain that before writing any code, we give Claude
> a persistent understanding of the project.

```
Read README.md and generate a CLAUDE.md file for this project.
It should cover: what we are building, the architecture, the tech stack,
the project structure we will create, and the coding conventions to follow.
The whole process will happen in the CLI — there are no API calls from the app.
Streamlit is only used for the investor form input and the final portfolio display.
All Claude calls happen through this CLI session via subagents and prompts.
```

---

## Stage 2 — Build the Investor Form

> Now we have context. Ask Claude to scaffold the form. Point out how CLAUDE.md
> shapes the output — it already knows the stack, the storage format, and the constraints.

```
Build a Streamlit investor questionnaire form. It should collect:
- investor name
- investment horizon
- risk tolerance
- liquidity needs
- annual return expectation
- preferences or constraints

Store each submission as a JSON object with a UUID and ISO-8601 timestamp,
appended to data/submissions.json. Create the file automatically if it does not exist.
Keep the form clean and minimal.
```

> Run the app and submit a test entry. Show students the resulting submissions.json.

```
streamlit run app.py
```

---

## Stage 3 — Slash Commands

### 3a. Show the pain first

> Type this prompt manually to screen a ticker. Tell students you need to do this
> for every asset in the universe — VOO, AGG, VTI, BND, QQQ, GLD...

```
Research the ETF with ticker VOO. Give me the following:

1. Full name and issuer
2. Investment strategy and asset class
3. Key holdings or market exposure
4. Risk profile — volatility and drawdown characteristics
5. Liquidity — approximate market cap or AUM and daily trading volume
6. Suitability — which investor risk profiles is this appropriate for (Conservative / Moderate / Aggressive)?
7. Verdict — should this be included in a robo-advisor asset universe, and why?

Return the result as a JSON object so I can save it to our asset universe file.
```

> Now say: "Let's do AGG." Start typing the same prompt again. Stop halfway.
> "This is exactly what slash commands are for."

### 3b. Create the /screen slash command

```
Create a slash command called "screen" in .claude/commands/screen.md.
It should take a ticker symbol as its argument and run the same research
prompt we just used for VOO. The command should append the result to
data/asset_universe.json, creating the file as an empty array if it does not exist.
```

> Show students the markdown file. Point out that it is just a prompt template
> with $ARGUMENTS as a placeholder. That is the whole mechanism.

> Now use the command to build the asset universe live:

```
/screen AGG
```
```
/screen VTI
```
```
/screen QQQ
```
```
/screen GLD
```

### 3c. Create the /add-investor slash command

> Explain: during development we need test investors constantly.
> Filling the Streamlit form every time is slow.

```
Create a slash command called "add-investor" in .claude/commands/add-investor.md.
It should generate a completely random but realistic investor persona each time
with no input required — vary age, background, risk profile, and goals.
The persona should match the submissions.json schema exactly and be appended to
data/submissions.json automatically.
```

> Test it:

```
/add-investor
```

---

## Stage 4 — Skills

### 4a. Show the problem first

> Ask Claude to profile an investor with no guidance. Show students the output.
> Point out: it is a few paragraphs of flowing text. No consistent fields.
> No JSON. Nothing a downstream agent could reliably parse.

```
Look at the latest submission in data/submissions.json and give me
a risk profile for this investor.
```

> "If the next agent needs to read this — where is the risk score?
> Where are the asset class weights? It doesn't know. It's just text.
> This is what a skill solves."

### 4b. Create the investor-profiler skill

```
Create a skill file at skills/investor-profiler/SKILL.md for an intake subagent.

This skill transforms a raw investor form submission into a structured risk profile.
It should:
- Derive a risk score from 1–10 by weighing horizon, risk tolerance, liquidity, and return expectation together
- Assign a risk label (Conservative, Moderate, Moderate-Aggressive, Aggressive)
- Flag and resolve any contradictions between inputs
- Parse constraints into separate exclusions and preferences lists
- Write a one-sentence plain-language profile summary

Output must be a strict JSON object with these fields:
name, risk_score, risk_label, investment_horizon_years, liquidity_priority,
return_expectation_pct, exclusions, preferences, contradictions_flagged, profile_summary.
```

> Now run the same prompt as before but tell Claude to use the skill:

```
Look at the latest submission in data/submissions.json and apply
the investor-profiler skill in skills/investor-profiler/SKILL.md
to produce a structured risk profile.
```

> Show the contrast. Structured JSON, consistent fields, contradictions surfaced.

### 4c. Create the asset-screener skill

```
Create a skill file at skills/asset-screener/SKILL.md for a market subagent.

This skill evaluates the asset universe against a specific investor risk profile
and returns a shortlist of suitable assets. It should:
- Evaluate each asset on risk alignment, constraint compliance, and return contribution
- Hard-exclude any asset that violates the investor's exclusions (score 0, include: false)
- Assign a suitability score from 1–10 per asset
- Return only included assets in the shortlist, with excluded assets listed separately

Output must be a strict JSON object with: investor_name, total_assets_evaluated,
shortlist (array with ticker, asset_class, suitability_score, fit_reasons, concerns, include),
and excluded (array with ticker and reason).
```

### 4d. Create the portfolio-constructor skill

```
Create a skill file at skills/portfolio-constructor/SKILL.md for a portfolio subagent.

This skill takes an investor risk profile and a screened asset shortlist and builds
a final portfolio allocation. It should:
- Assign weights that sum to exactly 100%
- Cap any single position at 40%
- Prefer higher suitability scores when choosing between similar assets
- Flag a diversification warning if fewer than 3 assets are available
- Check whether the portfolio can realistically meet the return expectation
- Write a one-sentence rationale per position

Output must be a strict JSON object with: investor_name, risk_label,
diversification_warning, return_expectation_met, return_expectation_note,
allocation (array with ticker, asset_class, weight_pct, rationale),
and asset_class_summary (equities_pct, fixed_income_pct, alternatives_pct).
All weights must sum to exactly 100.
```

### 4e. Create the report-writer skill

```
Create a skill file at skills/report-writer/SKILL.md for the master agent.

This skill synthesizes all upstream agent outputs into a final recommendation.
It should:
- Write a 3–5 sentence plain-language narrative covering who the investor is,
  why the portfolio fits their profile, and key risks
- Surface any warnings from upstream agents — never hide contradictions,
  diversification issues, or unmet return expectations
- Append the final result to data/portfolios.json

Output must be a strict JSON object with: id (UUID), generated_at (ISO-8601),
investor_name, risk_label, risk_score, narrative, warnings, allocation
(array with ticker, asset_class, weight_pct, rationale), asset_class_summary,
and a standard disclaimer.
```

---

## Stage 5 — Subagents

### 5a. Test a single subagent first

> Before running the full pipeline, test the intake subagent in isolation.
> Students watch the first subagent spawn in the terminal.

```
Spawn a subagent to act as the intake agent. It should:
- Read data/submissions.json and find the most recent entry
- Apply the investor-profiler skill in skills/investor-profiler/SKILL.md
- Return the structured risk profile
```

### 5b. Run the full pipeline

> "Now we chain them all together. One prompt. Four subagents.
> Watch the terminal."

```
Spawn a subagent to act as the intake agent. Read data/submissions.json,
find the most recent investor, and apply the investor-profiler skill in
skills/investor-profiler/SKILL.md to produce a structured risk profile.

Then spawn a second subagent to act as the market agent. Read
data/asset_universe.json and apply the asset-screener skill in
skills/asset-screener/SKILL.md against the risk profile to produce
a shortlist of suitable assets.

Then spawn a third subagent to act as the portfolio agent. Apply the
portfolio-constructor skill in skills/portfolio-constructor/SKILL.md
using the risk profile and screened shortlist to build a final allocation.

Finally, apply the report-writer skill in skills/report-writer/SKILL.md
to synthesize all three outputs into a final recommendation and append
it to data/portfolios.json.
```

### 5c. Turn it into a slash command

```
Create a slash command called "run-pipeline" in .claude/commands/run-pipeline.md.
It should take an investor name as its argument and run the full 4-subagent pipeline:
intake → market → portfolio → report, using the appropriate skill at each step,
and writing the final result to data/portfolios.json.
```

> Test it:

```
/run-pipeline [investor name]
```

---

## Stage 6 — Close the Loop

> "The pipeline writes to portfolios.json. Now we just need to display it."

```
Build a Streamlit dashboard page at pages/2_Portfolio.py that reads
data/portfolios.json and displays the most recent portfolio for a selected investor.

Show:
- A pie chart of the position allocation using Plotly
- A pie chart of the asset class breakdown
- The narrative from the master agent
- Any warnings as highlighted banners
- A table of positions with ticker, weight, and rationale
- The disclaimer at the bottom

Create portfolios.json as an empty array if it does not exist.
```

> Open the Streamlit app. Show the full loop: form → CLI → chart.

---

> **End of workshop.**
> The repository now contains a working robo-advisor built entirely from a README,
> using CLAUDE.md, slash commands, skills, and subagents.
