"""The Budget Agent will handle trip cost estimation and savings later."""

from __future__ import annotations

from agents import Agent




def build_budget_agent(config) -> Agent:
    return Agent(
        name="Budget Agent",
        model=config.llm_model,
        instructions=(
            "You are a specialist in an autonomous travel planning system.\n"
            "You are responsible for staying within the user's budget and avoiding unnecessary costs.\n"
        ),
        tools=[],
        handoffs=[],
    )

