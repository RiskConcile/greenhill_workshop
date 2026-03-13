# Build a Simple Robo‑Advisor with Claude Code

A hands-on workshop for Greenhill Capital exploring how **Claude Code** can help build a simple robo‑advisor prototype.

The goal is not to build a real investment product. The goal is to learn how Claude can help turn a repository into a working project using:

**README → CLAUDE.md → Web App → Slash Commands → Skills → Subagents**

---

# What you will build

During the workshop we will gradually build a small prototype:

1. Generate a **`CLAUDE.md`** file from the repository README
2. Build a **simple responsive investor intake form**
3. **Store incoming form submissions**
4. Create **slash commands** for repetitive workflows
5. Package workflows into reusable **skills**
6. Use **subagents** that collaborate to generate portfolio suggestions

---

# Core idea

The system will follow a simple workflow:

1. An investor submits preferences through a web form
2. The submission is stored
3. Agents analyze the information
4. Market information is gathered
5. A portfolio suggestion is generated

This demonstrates how **agent-based workflows** can be applied to financial use cases.

---

# Workshop roadmap

## 1. Generate `CLAUDE.md`

Claude reads the repository and generates a project instruction file.

Topics covered:

- What `CLAUDE.md` is
- Why it improves project consistency
- Generating it from `README.md`

---

## 2. Build the investor form

Create a simple responsive web form that collects:

- investment horizon
- risk tolerance
- liquidity needs
- return expectations
- preferences or constraints

Claude Code will scaffold and refine the UI.

---

## 3. Store submissions

Incoming form data will be captured and stored.

Possible approaches:

- JSON storage
- lightweight database
- simple API endpoint

This creates structured input for later agent processing.

---

## 4. Create slash commands

Slash commands simplify repeated prompting.

Example ideas:

- `/screen` – gather information on a security
- `/profile-risk` – summarize an investor profile
- `/compare-assets` – compare securities

These commands help standardize workflows.

---

## 5. Create skills

Skills package reusable capabilities so they can be reused across agents.

Example skills:

- Investor intake parsing
- Market screening
- Portfolio construction
- Report generation

---

## 6. Introduce subagents

Specialized agents collaborate on the workflow.

Example roles:

**Intake Agent** – reads investor submissions

**Market Agent** – gathers market data

**Portfolio Agent** – generates a candidate portfolio

**Master Agent** – coordinates the process

---

# Prototype workflow

```
Investor Form
      |
Submission Storage
      |
Intake Agent
      |
Market Agent + Portfolio Agent
      |
Master Agent
      |
Portfolio Recommendation
```

---

# Important note

This project is **for educational purposes only**. It is not financial advice and not a real robo‑advisor product.

---

# Possible extensions

Future versions could include:

- portfolio backtesting
- dashboards
- watchlists and alerts
- macro analysis agents
- ESG preference filters

---

# What students need

- GitHub
- Claude Code access
- basic web development familiarity

---

# Outcome

By the end of the workshop students will understand:

- how `CLAUDE.md` works
- how Claude can build and modify code
- how to design **skills and slash commands**
- how **subagents collaborate in a workflow**

---

Students are encouraged to experiment and extend the project beyond the workshop.

