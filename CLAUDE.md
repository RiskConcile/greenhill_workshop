# Robo-Advisor Workshop — Claude Code Native Workflow

## Purpose

This project is a **live workshop** showing how Claude Code's native features can build
a working application from scratch. We start with only a README and end with a functioning
robo-advisor, built step by step in the CLI in front of students.

The application is a simple robo-advisor. But the application is not the point.
The point is the workflow: **README → CLAUDE.md → slash commands → skills → subagents**.

This is not financial advice. This is an educational prototype.

---

## Architecture

Streamlit plays a minimal role — it is a thin wrapper at each end of the pipeline:

```
[Streamlit Form]  →  submissions.json  →  [CLI / Claude Code Session]  →  portfolios.json  →  [Streamlit Dashboard]
  (investor input)                          (where the workshop lives)                          (pie chart + summary)
```

Everything in the middle — screening assets, profiling investors, spawning subagents,
constructing the portfolio — happens **in the Claude Code CLI**.

There are no Python agent files. The agent logic lives in the skills and in the prompts.
Subagents are spawned directly by the master agent prompt inside a Claude Code session.

---

## Data Flow

```
data/
├── submissions.json     # Written by Streamlit form; read by the pipeline
├── asset_universe.json  # Built live during the workshop using /screen
└── portfolios.json      # Written by the master agent; read by Streamlit dashboard
```

---

## Project Structure

```
greenhill-workshop/
├── CLAUDE.md                          # This file
├── README.md                          # Workshop overview
├── app.py                             # Streamlit: form input + portfolio display
├── data/
│   ├── submissions.json
│   ├── asset_universe.json
│   └── portfolios.json
├── .claude/
│   └── commands/                      # Slash commands (instructor dev tools)
│       ├── add-investor.md
│       ├── screen.md
│       ├── profile-risk.md
│       ├── compare-assets.md
│       └── run-pipeline.md
└── skills/                            # Reasoning frameworks for subagents
    ├── investor-profiler/SKILL.md
    ├── asset-screener/SKILL.md
    ├── portfolio-constructor/SKILL.md
    └── report-writer/SKILL.md
```

---

## Workshop Progression

Build in this order. Each stage is done live in the CLI with students watching.

1. **CLAUDE.md** — establish project context (this file, generated from README)
2. **Streamlit form** — simple questionnaire: horizon, risk tolerance, liquidity, goals
3. **Submission storage** — form writes to `data/submissions.json`
4. **Asset universe** — use `/screen` to research a handful of ETFs and build `asset_universe.json`
5. **Slash commands** — introduced as repetition becomes obvious during stages 2–4
6. **Skills** — introduced when agent output is shallow or inconsistent; refine them live
7. **Subagents** — the master agent prompt spawns all subagents; students watch in the terminal
8. **Streamlit dashboard** — reads `portfolios.json` and renders the final portfolio as a pie chart

---

## Slash Commands

Slash commands are instructor tools that eliminate repetitive prompts during the build.
They live in `.claude/commands/` and are invoked with `/command-name` in the CLI.

| Command | Purpose | When it appears |
|---|---|---|
| `/add-investor` | Scaffold a realistic test investor and append to `submissions.json` | Stage 2–3, when you need personas to test with |
| `/screen <ticker>` | Research a security and add a structured entry to `asset_universe.json` | Stage 4, building the asset universe live |
| `/profile-risk <name>` | Read a stored submission and produce a concise risk profile | Stage 5–6, checking how an investor would be interpreted |
| `/compare-assets <a> <b>` | Side-by-side comparison of two securities; recommend which to include | Stage 4, when choosing between similar ETFs |
| `/run-pipeline <name>` | Spawn all subagents for a named investor and print the final recommendation | Stage 7, the full end-to-end demo |

---

## Skills

Skills are reusable reasoning frameworks that subagents carry into their work.
They live in `skills/` and define *how* an agent should think, not just what to produce.
They are introduced and refined live during the workshop when raw agent output falls short.

### `investor-profiler`
Used by the **intake subagent**.
Transforms a raw form submission into a structured risk profile: risk score, horizon,
liquidity needs, return expectations, constraints. Output is JSON.

### `asset-screener`
Used by the **market subagent**.
Evaluates a single asset against an investor profile: strategy fit, risk alignment,
cost, liquidity, and a suitability rating. Ensures consistent, comparable output
across all assets in the universe.

### `portfolio-constructor`
Used by the **portfolio subagent**.
Given a risk profile and screened assets, builds a target allocation: asset class weights,
position weights, rationale per decision, constraints respected or flagged.

### `report-writer`
Used by the **master agent**.
Synthesizes all upstream outputs into a client-facing narrative: plain-language summary,
reasoning, risks acknowledged, and a disclaimer. Also writes the result to `portfolios.json`
so Streamlit can display it.

---

## Subagent Architecture

The master agent is invoked with a single prompt in the Claude Code CLI.
It spawns three subagents using the Agent tool, collects their outputs,
and synthesizes the final recommendation.

```
Master Agent
├── spawns → Intake Subagent     (uses investor-profiler skill)
├── spawns → Market Subagent     (uses asset-screener skill)
├── spawns → Portfolio Subagent  (uses portfolio-constructor skill)
└── synthesizes → Final Report   (uses report-writer skill → writes portfolios.json)
```

Students watch each subagent being spawned in the terminal in real time.
This is the moment the workshop builds toward.

---

## Tech Stack

- **Python**: 3.10+
- **UI**: Streamlit — no Anthropic SDK, no API calls, pure UI only
- **Visualization**: Plotly (pie charts for portfolio breakdown)
- **Storage**: Plain JSON files in `data/`
- **All Claude calls**: Made exclusively through the Claude Code CLI session via subagents and prompts — never from application code

---

## Conventions

- Keep Streamlit minimal — form fields in, chart out, nothing else
- All data is plain JSON with ISO-8601 timestamps
- Skills are markdown files — they are prompts, not code
- Slash commands are markdown files — they are prompt templates, not code
- When in doubt, put logic in the prompt, not in Python
- In the process of building the Robo advisor, you can ask the user anything in order to clarify or understand the concept of something.
