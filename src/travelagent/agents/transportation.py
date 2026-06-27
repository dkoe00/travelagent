"""The Transportation Agent will handle transit and route planning later."""

from __future__ import annotations

from agents import Agent, function_tool, handoff


@function_tool
def geocode_location(query: str, city: str | None = None):
    pass

@function_tool
def estimate_route(origin: str, destination: str, mode: str):
    pass

@function_tool
def compare_transport_modes(origin: str, destination: str):
    pass


def build_transportation_agent(config, coordinator_agent: Agent) -> Agent:
    return Agent(
        name="Transportation Agent",
        model=config.llm_model,
        instructions=(
            "You are a specialist in an autonomous travel planning system.\n"
            "You are responsible for finding routes between locations and calculating travel times.\n"
            "Use your tools where they are needed and hand off to the coordinator with your results or when you are stuck."
        ),
        tools=[],
        handoffs=[handoff(coordinator_agent)],
    )