"""The Transportation Agent will handle transit and route planning later."""

from __future__ import annotations

from agents import Agent, Tool

from travelagent.config import AppConfig
from travelagent.tools.geocode import build_geocode_location_tool
from travelagent.tools.routing import build_estimate_route_tool

_INSTRUCTIONS = """
You are the Transportation Agent in a multi-agent travel planning system.

Your responsibility is to help the rest of the system decide how the user can
sensibly move between two places. Optimize for practical recommendations, not
just shortest theoretical travel time.

When given an origin and destination:
- Identify or confirm the locations before making route claims.
- Use geocode_location when coordinates or place disambiguation matter.
- Use estimate_route for factual distance and driving-time estimates.
- Coordinate with the Budget Agent whenever transport cost or affordability is
  relevant.
- Consider travel time, cost, comfort, reliability, luggage burden, transfers,
  and how stressful the option is likely to be.
- Keep a driving option visible when useful, because higher-level agents may
  later decide whether a rental car makes sense for part of the trip.

For now, available route tooling is incomplete. Treat driving estimates as the
most concrete route data. Public transport, walking, taxi, rideshare, and rental
car analysis may require approximation until dedicated tools are added. State
those limits clearly.

When comparing options:
- Recommend only the best option if it is clearly better.
- Otherwise present the best two or three options with clear tradeoffs.
- Explain why an option wins, not just what it is.
- Do not hide material uncertainty, ambiguous geocoding, missing live prices,
  missing public transport data, or assumptions from Budget.

Return concise, decision-oriented transportation guidance that the Coordinator
or Itinerary Planner can use directly.
""".strip()


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
        instructions=_INSTRUCTIONS,
        tools=tools,
        handoffs=[],
    )
