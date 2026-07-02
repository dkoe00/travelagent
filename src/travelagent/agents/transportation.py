"""The Transportation Agent will handle transit and route planning later."""

from __future__ import annotations

from agents import Agent, Tool

from travelagent.config import AppConfig
from travelagent.tools.geocode import build_geocode_location_tool
from travelagent.tools.routing import build_estimate_route_tool


def build_transportation_agent(
    config: AppConfig,
    budget_agent: Agent[object],
) -> Agent[object]:
    tools: list[Tool] = [
        build_geocode_location_tool(config),
        build_estimate_route_tool(config),
    ]
    # TODO @dkoe00: Add typed budget-agent parameters.
    tools.append(
        budget_agent.as_tool(
            tool_name="budget_agent",
            tool_description=(
                "Estimate transportation costs and explain budget tradeoffs "
                "for route options."
            ),
        )
    )

    return Agent(
        name="Transportation Agent",
        model=config.llm_model,
        instructions=(
            "You are a specialist in an autonomous travel planning system.\n"
            "You are responsible for finding routes between locations and calculating travel times.\n"
            "Use the geocode_location tool before making claims about exact coordinates.\n"
            "Use estimate_route when the user needs a travel time or distance between places.\n"
            "Use the Budget Agent when transportation cost estimates or budget tradeoffs matter.\n"
            "Explain uncertainty when geocoding returns multiple plausible candidates."
        ),
        tools=tools,
        handoffs=[],
    )
