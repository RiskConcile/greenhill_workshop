"""
Base Agent Utilities
=====================
Shared client, model config, and helpers used by all agents.

The Anthropic API key is read from:
  1. st.session_state["api_key"]  (set in the Streamlit sidebar)
  2. ANTHROPIC_API_KEY environment variable
"""

import json
import os
import re
from anthropic import Anthropic

# ── Defaults ────────────────────────────────────────────────
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096


def get_client(api_key: str | None = None) -> Anthropic:
    """Return an Anthropic client, preferring an explicit key."""
    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError(
            "No API key found. Set ANTHROPIC_API_KEY or enter it in the sidebar."
        )
    return Anthropic(api_key=key)


def call_llm(
    system: str,
    user_message: str,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_TOKENS,
    temperature: float = 0.3,
) -> str:
    """
    Simple single-turn LLM call.

    Returns the assistant's text response.
    """
    client = get_client(api_key)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def call_llm_json(
    system: str,
    user_message: str,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_TOKENS,
    temperature: float = 0.2,
) -> dict:
    """
    Call the LLM and parse the response as JSON.

    The system prompt should instruct the model to return valid JSON.
    Extracts JSON from markdown code fences if present.
    """
    raw = call_llm(system, user_message, api_key, model, max_tokens, temperature)

    # Try to extract JSON from code fences first
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", raw, re.DOTALL)
    json_str = fence_match.group(1).strip() if fence_match else raw.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Fallback: find the first { ... } or [ ... ] block
        brace_match = re.search(r"[\[{].*[\]}]", json_str, re.DOTALL)
        if brace_match:
            return json.loads(brace_match.group())
        raise ValueError(f"Could not parse LLM response as JSON:\n{raw[:500]}")


def call_llm_with_tools(
    system: str,
    user_message: str,
    tools: list[dict],
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_TOKENS,
) -> tuple[str, list[dict]]:
    """
    Call the LLM with tool definitions.

    Returns (text_response, list_of_tool_calls).
    Each tool call is: {"name": str, "input": dict, "id": str}
    """
    client = get_client(api_key)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.2,
        system=system,
        tools=tools,
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = []
    tool_calls = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "tool_use":
            tool_calls.append({
                "name": block.name,
                "input": block.input,
                "id": block.id,
            })

    return "\n".join(text_parts), tool_calls