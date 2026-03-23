# Workshop Outline — Robo-Advisor with Claude Code Native Features

> Core pedagogical arc: students feel the problem before seeing the solution.
> Each Claude feature is introduced at the moment of pain, not before.

---

## Stage 1 — Project Context
**What:** Generate `CLAUDE.md` from the README
**Feature:** `CLAUDE.md`
**The lesson:** Show Claude responding to the same prompt with and without CLAUDE.md.
Students see how context shapes behavior. Sets the tone: *you are programming Claude's
understanding of the project, not just writing code.*

---

## Stage 2 — Data Collection
**What:** Build the Streamlit investor questionnaire form
**Feature:** Claude Code building and editing code
**The lesson:** Claude reads the project structure, understands conventions from CLAUDE.md,
and scaffolds the form. Students see how CLAUDE.md already pays off here.

---

## Stage 3 — Slash Commands
**What:** Use `/screen` to research ETFs and build the asset universe live.
Use `/add-investor` to create test personas.
**Feature:** Slash commands (`.claude/commands/`)
**The lesson:** By now students have typed similar prompts 3–4 times.
Introduce slash commands as the solution. Show the markdown file, show how it
parameterizes the prompt. *A slash command is just a reusable prompt template.*

---

## Stage 4 — Skills
**What:** Build `investor-profiler` and `asset-screener` skills. Run them manually, show output.
**Feature:** Skills
**The lesson:** Ask Claude to profile an investor without a skill — output is vague and
inconsistent. Add the skill and run again — output is structured, typed, reliable.
*A skill is a reasoning framework, not code.*

---

## Stage 5 — Subagents
**What:** Write the master agent prompt. Spawn the full pipeline for a test investor in the CLI.
**Feature:** Subagents (Agent tool)
**The lesson:** The climax. Students watch intake → market → portfolio subagents spawn
in the terminal, each carrying a skill, each writing its output.
*This is what agentic actually means — Claude delegating to Claude.*

---

## Stage 6 — Close the Loop
**What:** Build the Streamlit dashboard to read `portfolios.json` and render a pie chart.
**Feature:** Claude building visualization code
**The lesson:** Lightweight closer. Shows the full loop: form → CLI → chart.
The sophistication was in the middle, not the endpoints.

---

## Feature Progression

| Stage | Feature |
|---|---|
| 1 | `CLAUDE.md` — project context |
| 2 | Code generation — scaffolding from context |
| 3 | Slash commands — reusable prompt templates |
| 4 | Skills — structured reasoning frameworks |
| 5 | Subagents — autonomous delegation |
| 6 | Visualization — closing the loop |

---

## Key Design Decisions

- Streamlit is a thin bookend only — form input and pie chart output
- No Anthropic SDK in application code — all Claude calls via CLI session
- No `agents/` Python folder — agent logic lives in skills and prompts
- Asset universe is built live during Stage 3 using `/screen` (kept simple)
- Data flow: `submissions.json` → pipeline → `portfolios.json`
