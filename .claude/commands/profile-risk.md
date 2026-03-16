Analyze the investor profile using our LLM-powered intake agent.

Read the file `data/submissions.json` and find the submission matching: $ARGUMENTS
(match by name, partial name, or "latest" for the most recent submission).

Then run the **Intake Agent** programmatically using a subagent:

```python
import json
from agents.intake_agent import analyze_investor_profile

# Load the target submission
with open("data/submissions.json") as f:
    submissions = json.load(f)

# Find the matching submission (latest if no match found)
target = submissions[-1]  # default to latest

# Run the LLM-powered intake agent
profile = analyze_investor_profile(target, api_key="<from env ANTHROPIC_API_KEY>")
print(json.dumps(profile, indent=2))
```

After getting the agent output, present:

1. **Risk Score & Label** — from the LLM analysis (NOT a formula)
2. **LLM Reasoning** — why the agent chose this score (this is the key differentiator from rules-based!)
3. **Profile Summary** — the agent's natural language understanding
4. **Flags** — any inconsistencies or warnings the agent detected
5. **Suggested approach** — based on the profile, what asset mix makes sense

Compare the LLM output to what a simple rule-based system would produce.
Highlight where the LLM adds value (e.g., interpreting free-text preferences,
catching contradictions between stated risk tolerance and actual horizon).

This demonstrates **why LLM agents are better than rules** for nuanced tasks.

Format the output clearly with headers. Educational purposes only.