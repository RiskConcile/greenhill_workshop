# CLAUDE.md — Greenhill Workshop: Simple Robo-Advisor

## What we are building

A hands-on workshop prototype that demonstrates how Claude Code can help build a simple robo-advisor using agent-based workflows. The end product is **not** a real investment product — it is an educational system that shows how AI agents can collaborate on a financial use case.

The full workflow:
1. An investor submits preferences through a Streamlit form
2. The submission is stored as JSON
3. Subagents (running inside this CLI session) analyze the data, gather market context, and produce a portfolio suggestion
4. The result is displayed back to the investor via a Streamlit output page

---

## Architecture

All intelligence lives in the CLI. There are no API calls made from within the application code. Claude Code itself is the runtime — subagents are spawned as part of this session.

```
Streamlit Form (input)
        |
  data/portfolios.json  (storage)
        |
  CLI Session (Claude Code)
        |
   ┌────┴────────────────────┐
   │                         │
Intake Agent          Market Agent
   │                         │
   └────────┬────────────────┘
            │
      Portfolio Agent
            │
      Master Agent (coordinator)
            │
  Streamlit Display (output)
```

- **Streamlit** is used only at the boundary: intake form and final display.
- **All Claude calls happen through this CLI session** via subagents and slash commands / skills.
- **Storage** is a flat JSON file (`data/portfolios.json`).

---

## Tech stack

| Layer | Technology |
|---|---|
| UI | Streamlit (Python) |
| Storage | JSON file (`data/portfolios.json`) |
| Agent runtime | Claude Code CLI (this session) |
| Language | Python 3 |
| Environment | `.venv` (virtualenv, managed locally) |
| Python version | see `.python-version` |

---

## Project structure

```
greenhill_workshop/
├── CLAUDE.md                  # This file — project instructions for Claude
├── README.md                  # Workshop overview
├── .python-version            # Pinned Python version
├── .venv/                     # Local virtual environment (not committed)
├── agents/                    # Agent prompt files and logic
│   ├── intake_agent.md        # Intake Agent: parses investor submission
│   ├── market_agent.md        # Market Agent: gathers market context
│   ├── portfolio_agent.md     # Portfolio Agent: constructs candidate portfolio
│   └── master_agent.md        # Master Agent: coordinates all subagents
├── data/
│   └── portfolios.json        # Stored investor submissions and results
├── commands/                  # Slash command definitions (.md files)
│   ├── screen.md              # /screen — gather info on a security
│   ├── profile-risk.md        # /profile-risk — summarize an investor profile
│   └── compare-assets.md      # /compare-assets — compare securities
├── skills/                    # Reusable skill definitions
│   ├── intake-parsing.md
│   ├── market-screening.md
│   ├── portfolio-construction.md
│   └── report-generation.md
├── app/
│   ├── form.py                # Streamlit investor intake form
│   └── display.py             # Streamlit portfolio result display
└── .claude/
    └── settings.local.json    # Claude Code local permissions
```

---

## Coding conventions

### General
- Keep files small and single-purpose.
- Prefer plain Python — no unnecessary frameworks or abstractions.
- No external API calls from application code. All AI work happens through Claude Code CLI.

### Python
- Use Python 3 with the version pinned in `.python-version`.
- Use the local `.venv` for dependencies; do not install globally.
- Use `snake_case` for variables and functions, `PascalCase` for classes.
- No type annotations unless the logic genuinely benefits from them.
- No docstrings on simple functions — let the code speak for itself.

### Storage
- Investor submissions are stored in `data/portfolios.json` as a JSON array.
- Each entry should include at minimum: `name`, `timestamp`, and the form fields.
- Do not use a database. JSON file storage is intentional for workshop simplicity.

### Streamlit
- Use Streamlit only for the intake form (`app/form.py`) and the result display (`app/display.py`).
- No business logic in Streamlit files — they read from and write to `data/portfolios.json` only.

### Agents
- Each agent is defined by a prompt file in `agents/`.
- Agents are spawned as subagents within this Claude Code CLI session.
- The Master Agent coordinates all others; individual agents should be focused and single-responsibility.
- Agent prompt files use Markdown with a clear `# Role`, `# Input`, `# Task`, and `# Output` structure.

### Slash commands and skills
- Slash command files live in `.claude/commands/` (project-scoped) or `~/.claude/commands/` (global).
- Skill files follow the same pattern but are reusable across agents.
- Name commands and skills using `kebab-case`.

### What not to do
- Do not add error handling for scenarios that cannot happen in this prototype.
- Do not design for hypothetical future requirements (backtesting, dashboards, etc.).
- Do not call external APIs or LLMs from within the Python application code.
- Do not commit `.venv/`, secrets, or API keys.

---

## Educational disclaimer

This project is for educational purposes only. It is not financial advice and not a real robo-advisor product.
