# Build a Simple Robo-Advisor with Claude Code

A hands-on workshop for Greenhill Capital on building a Robo-advisor prototype with **Claude Code**.

This workshop is not about building a production-grade investment platform. It is about learning how to use Claude Code as a practical engineering partner to go from **idea → repository → project instructions → web app → commands → skills → subagents**.

Along the way, we will design a simple workflow where:

- an investor fills out a responsive web form,
- the submission is stored,
- specialized agents process the information,
- market-monitoring agents gather context,
- a portfolio agent proposes a tailored allocation,
- and a master agent combines everything into a final output.

## Who this workshop is for

This workshop is designed for:

- Finance students curious about AI-assisted software building
- Students who want to understand agentic workflows in a practical setting
- Beginners who want to see how a GitHub repo can become a working prototype with Claude Code

You do **not** need to be an expert software engineer to follow along. Basic familiarity with GitHub, web apps, and finance concepts is enough.

## What you will build

By the end of the workshop, students will have explored a prototype project with the following components:

1. **A GitHub-based starter repository**
2. **A **``** file** generated from the repository context
3. **A simple responsive investor intake form**
4. **A way to collect and store incoming investor submissions**
5. **Custom slash commands** for repetitive workflows
6. **Skills** to package reusable capabilities
7. **Subagents** that collaborate on analysis and portfolio generation

## Learning goals

After completing the workshop, students should be able to:

- understand the purpose of `CLAUDE.md`
- generate and refine `CLAUDE.md` from repository documentation such as `README.md`
- use Claude Code to scaffold and improve a web app
- build a simple input workflow for collecting investor preferences and risk tolerance
- think about structured financial workflows in terms of reusable commands and skills
- understand how subagents can specialize and collaborate
- design a simple multi-agent robo-advisor architecture

---

# Workshop roadmap

## Part 1 — From GitHub repo to `CLAUDE.md`

We begin with the existing GitHub repository.

### Objective

Show students how Claude can inspect the repository documentation and generate a project-aware `CLAUDE.md` file.

### What we will cover

- What `CLAUDE.md` is
- Why `CLAUDE.md` matters for consistent project behavior
- How Claude can infer project context from `README.md`
- How to iterate on the generated `CLAUDE.md`

### Key idea

Instead of repeatedly re-explaining the same project context, goals, conventions, and constraints, we place them in `CLAUDE.md` so Claude Code can operate with stronger project awareness.

### Example topics for the `CLAUDE.md`

- project purpose
- coding conventions
- UI goals
- folder structure expectations
- financial disclaimers
- preferred stack
- workshop scope
- what the AI should and should not do

---

## Part 2 — Build a simple responsive investor intake form

Next, we will use Claude Code to create a simple web app.

### Objective

Build a clean, responsive form that collects investor preferences.

### Example fields

- name or investor ID
- age bracket
- investment horizon
- target return expectations
- liquidity needs
- loss tolerance
- experience level
- ethical or sector preferences
- preferred asset classes
- free-text notes

### Design goals

- simple and modern UI
- mobile-friendly layout
- clear form validation
- structured outputs for downstream processing

### Why this matters

The quality of downstream agentic analysis depends heavily on the quality and structure of the incoming data.

---

## Part 3 — Collect and save form submissions

Once the form exists, the next step is handling real inputs.

### Objective

Show how incoming form data can be captured and stored.

### Possible implementation options

- save to a local JSON file
- save to a lightweight database
- send to an API endpoint
- log to a spreadsheet-like backend

### Teaching angle

This is an important bridge between **front-end interaction** and **agent workflow orchestration**.

Students will see that once data is captured reliably, it can be passed into automated analysis pipelines.

---

## Part 4 — Simplify repetitive work with slash commands

As the project grows, prompts can become repetitive.

### Objective

Introduce slash commands as a practical abstraction layer for recurring tasks.

### Example idea

A command such as `/screen` could:

- open a market data source such as Yahoo Finance
- inspect a chosen security
- capture a summary or snapshot
- return structured output for further analysis

### Other possible command ideas

- `/profile-risk` → summarize an investor’s risk profile
- `/summarize-form` → convert raw intake data into structured advisor notes
- `/compare-assets` → compare a shortlist of securities
- `/rebalance-draft` → generate a draft reallocation based on new constraints
- `/portfolio-brief` → produce a short investment memo

### Teaching angle

Students will learn that slash commands are not just shortcuts. They are a way to create **repeatable, reusable workflows**.

---

## Part 5 — Package workflows as skills

Once commands become useful, we can formalize them into skills.

### Objective

Show how skills help isolate capabilities for future reuse.

### Why skills matter

Skills make it easier to:

- standardize repeated tasks
- separate responsibilities
- improve maintainability
- allow subagents to access specialized capabilities

### Example skill ideas

- **Investor Intake Skill** — parse and validate form submissions
- **Market Screening Skill** — gather and summarize security data
- **Portfolio Construction Skill** — map investor profiles to candidate allocations
- **Report Generation Skill** — turn outputs into readable portfolio summaries

### Teaching angle

This is the moment where the workshop moves from “prompting” into **system design**.

---

## Part 6 — Introduce subagents

This is where the project becomes truly agentic.

### Objective

Demonstrate how multiple specialized subagents can collaborate on a finance workflow.

### Example subagent roles

#### 1. Intake Agent

Responsible for:

- reading new form submissions
- extracting structured investor preferences
- cleaning and normalizing the data

#### 2. Market Monitor Agent

Responsible for:

- monitoring selected securities
- checking current market context
- gathering relevant facts or snapshots

#### 3. Portfolio Agent

Responsible for:

- translating investor preferences into a candidate portfolio
- aligning allocation logic with risk tolerance
- generating rationale for the proposed portfolio

#### 4. Master Agent

Responsible for:

- orchestrating the workflow
- delegating to subagents
- combining their outputs
- generating the final recommendation package

### Teaching angle

Students will see how specialization improves clarity, modularity, and scalability.

---

## Part 7 — End-to-end robo-advisor prototype flow

By combining all pieces, we arrive at a simple prototype pipeline:

1. Investor visits the web app
2. Investor submits preferences and risk profile
3. Submission is stored
4. Intake Agent reads and structures the submission
5. Market Monitor Agent gathers relevant market context
6. Portfolio Agent proposes a tailored portfolio
7. Master Agent combines the outputs
8. A final portfolio summary is produced

This is the central idea of the workshop: **turning a finance use case into an agentic system with Claude Code**.

---

# Suggested workshop agenda

## Session 1 — Project setup and `CLAUDE.md`

- Introduce the workshop vision
- Review the GitHub repository
- Explain what `CLAUDE.md` is
- Generate `CLAUDE.md` from `README.md`
- Refine the generated file together

## Session 2 — Build the form web app

- Define the required investor fields
- Scaffold the UI with Claude Code
- Make the form responsive
- Add validation and structure the outputs

## Session 3 — Handle incoming submissions

- Decide how to store submissions
- Create a simple persistence layer
- Test end-to-end submission flow

## Session 4 — Create slash commands

- Identify repetitive prompting patterns
- Design custom commands
- Test commands on realistic finance tasks

## Session 5 — Build skills

- Package repeated workflows into skills
- Separate responsibilities cleanly
- Prepare skills for later agent reuse

## Session 6 — Orchestrate subagents

- Define agent roles
- Connect agents through clear inputs and outputs
- Demonstrate a master/subagent workflow

## Session 7 — Demo and discussion

- Run the robo-advisor prototype
- Review strengths and limitations
- Discuss extensions and future ideas

---

# Example architecture

```text
[Investor Web Form]
        |
        v
[Submission Storage]
        |
        v
[Intake Agent] -----> [Structured Investor Profile]
        |
        +-----> [Master Agent] <----- [Market Monitor Agent]
                              |
                              v
                     [Portfolio Agent]
                              |
                              v
                  [Final Portfolio Recommendation]
```

---

# Important note on finance and responsibility

This workshop is for **educational purposes**.

The robo-advisor built here is a prototype for learning how Claude Code, skills, slash commands, and subagents can work together. It is **not** investment advice, not a regulated advisory product, and not a substitute for professional financial, legal, or compliance review.

Any real-world implementation would require much deeper work on:

- suitability assessment
- risk disclosures
- compliance and regulation
- data privacy
- security
- portfolio methodology
- auditability and monitoring

---

# Why this workshop is exciting

This project sits at the intersection of:

- finance
- software building
- AI-assisted development
- workflow design
- multi-agent systems

Students will not only learn how to build a small app. They will learn how to think in terms of:

- system instructions
- reusable abstractions
- specialized capabilities
- orchestration patterns

That makes this a powerful introduction to the future of AI-assisted financial tooling.

---

# Ideas for future extensions

To make the project even more interesting, future iterations could include:

- portfolio backtesting
- scenario analysis
- macroeconomic commentary agents
- watchlists and alerts
- document generation for investment memos
- user dashboards
- authentication and user accounts
- model portfolios by risk band
- ESG preference filters
- explainability modules for portfolio decisions
- compliance-aware output checks

---

# What students should prepare

Before the workshop, students should ideally have:

- access to GitHub
- access to Claude Code
- a basic understanding of HTML/CSS/JavaScript or a web framework
- interest in finance workflows and AI tools

---

# Expected outcomes

By the end of the workshop, students should walk away with:

- a clearer understanding of `CLAUDE.md`
- a working prototype repository structure
- a simple investor intake app
- exposure to slash commands and skills
- an intuition for subagent collaboration
- a practical framework for building future AI-assisted finance tools

---

# Closing thought

The ideas here are intentionally expansive.

A simple form can become a full workflow. A repeated prompt can become a slash command. A command can become a skill. A skill can empower a subagent. A group of subagents can become a working financial system prototype.

That is the journey this workshop is designed to make visible.

---

## Maintainer note

This repository and workshop will likely evolve over time. Students are encouraged to experiment, improve the flows, and extend the prototype in their own direction.

The best way to use this workshop is not just to copy it, but to build on top of it.

