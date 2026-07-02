"""The Budget Agent will handle trip cost estimation and savings later."""

from __future__ import annotations

from agents import Agent

from travelagent.tools.budget import build_estimate_transport_cost_tool


def build_budget_agent(config) -> Agent:
    # TODO @dkoe00: Add full-trip budget tools.
    return Agent(
        name="Budget Agent",
        model=config.llm_model,
        instructions=(
            "You are a specialist in an autonomous travel planning system.\n"
            "You are responsible for staying within the user's budget and avoiding unnecessary costs.\n"
            "Use estimate_transport_cost for transportation cost estimates.\n"
            "State clearly when costs are heuristic estimates rather than live prices."
        ),
        tools=[build_estimate_transport_cost_tool()],
        handoffs=[],
    )
