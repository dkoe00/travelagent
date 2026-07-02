"""The Transportation Agent will handle transit and route planning later."""

from __future__ import annotations

from agents import Agent

from travelagent.tools.geocode import build_geocode_location_tool
from travelagent.tools.routing import build_estimate_route_tool


def build_transportation_agent(config) -> Agent:
    return Agent(
        name="Transportation Agent",
        model=config.llm_model,
        instructions=(
            "You are a specialist in an autonomous travel planning system.\n"
            "You are responsible for finding routes between locations and calculating travel times.\n"
            "Use the geocode_location tool before making claims about exact coordinates.\n"
            "Use estimate_route when the user needs a travel time or distance between places.\n"
            "Explain uncertainty when geocoding returns multiple plausible candidates."
        ),
        tools=[
            build_geocode_location_tool(config),
            build_estimate_route_tool(config),
        ],
        handoffs=[],
    )
