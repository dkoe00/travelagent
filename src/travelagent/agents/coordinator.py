"""The Coordinator Agent will be defined here later."""

from __future__ import annotations

from agents import Agent


def build_coordinator_agent(config) -> Agent:
    """Build the Coordinator Agent for the terminal-only prototype."""
    # TODO @dkoe00: Wire transportation and budget agents.
    return Agent(
        name="Coordinator Agent",
        model=config.llm_model,
        instructions=(
            "You are the Coordinator Agent for a terminal-only Travel Planning "
            "Assistant prototype. Help plan trips clearly and concisely. "
            "Focus on practical travel guidance and keep responses brief when possible. "
            "Do not use tools."
        ),
    )
