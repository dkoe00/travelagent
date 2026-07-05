"""The Transportation Agent will handle transit and route planning later."""

from __future__ import annotations

from agents import Agent, Tool

from travelagent.config import AppConfig
from travelagent.agents.budget import build_budget_agent
from travelagent.schemas.transportation import TransportationAgentOutput
from travelagent.tools.geocode import build_geocode_location_tool
from travelagent.tools.routing import (
    build_compare_transport_options_tool,
    build_estimate_route_tool,
)

_INSTRUCTIONS = """
You are the Transportation Agent in a multi-agent travel planning system.

Your responsibility is to help the rest of the system decide how the user can
sensibly move between two places. Optimize for practical recommendations, not
just shortest theoretical travel time.

You are normally called as a tool by the Coordinator after destinations and
points of interest have already been identified. Treat named places in the
request as the intended route stops unless they are ambiguous.

When given a places pool from find_places():
- Treat the listed activities, restaurants, cafes, and accommodation options as
  candidate itinerary stops.
- Do not route every possible pair unless the pool is very small. Focus on
  itinerary-shaping information: likely area clusters, difficult transfers,
  sensible sequencing constraints, and practical transfer buffers.
- Use each place's area field to create TransportAreaCluster entries. Cluster
  nearby or same-area places together so the Itinerary Agent can build days with
  less criss-crossing.
- Use compare_transport_options for representative or important movements: likely
  accommodation/start area to major clusters, far-apart clusters, airport/station
  transfers if mentioned, and any movement that could affect feasibility.
- If accommodation is unknown, make a reasonable central-start assumption and add
  an unresolved_questions entry if the exact start point materially affects the plan.
- Flag places or areas that should not be casually combined in one day as
  LongTransferWarning entries.
- Add TransferBuffer entries for important movements the Itinerary Agent is likely
  to schedule.
- Add TransportSequenceConstraint entries when order matters, for example "visit
  these places on the same day", "avoid pairing these areas", or "schedule this
  after the nearby lunch/dinner area".

When given an origin and destination:
- Identify or confirm the locations before making route claims.
- Use geocode_location when coordinates or place disambiguation matter.
- Use compare_transport_options as the default tool for deciding how to travel
  between two places.
- Use estimate_route only when you need a single driving distance or driving
  time estimate.
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

When returning your final answer, use the structured output schema:
- Put one TransportationLegPlan in legs for each movement you evaluated.
- Put the best option for each leg in recommendation.recommended_option.
- Put useful alternatives in alternatives, not in prose only.
- Fill area_clusters with groupings the Itinerary Agent should use to build days.
- Fill sequence_constraints with concrete ordering or grouping rules.
- Fill transfer_buffers with minimum minutes the Itinerary Agent should reserve
  between important stops.
- Fill long_transfer_warnings with movements that risk making a day unrealistic.
- Use budget_notes for cost caveats that the Coordinator must preserve.
- Use itinerary_constraints for constraints such as long transfer time, walking
  burden, airport/station buffer, or rental-car implications.
- Use unresolved_questions when the Coordinator needs to ask the user or another
  agent for missing context.

Return concise, decision-oriented transportation guidance that the Coordinator
or Itinerary Planner can use directly.
""".strip()


def build_transportation_agent(
    config: AppConfig,
) -> Agent[object]:
    budget_agent = build_budget_agent(config)
    tools: list[Tool] = [
        build_geocode_location_tool(config),
        build_estimate_route_tool(config),
        build_compare_transport_options_tool(config),
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
        output_type=TransportationAgentOutput,
    )
