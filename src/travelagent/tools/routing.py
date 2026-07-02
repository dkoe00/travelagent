"""Routing tools for the Transportation Agent."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agents import function_tool

from travelagent.config import AppConfig
from travelagent.schemas.budget import TransportCostEstimate
from travelagent.schemas.transportation import (
    Geolocation,
    RouteEstimate,
    TransportMode,
    TransportOption,
    TransportOptionScore,
    TransportRecommendation,
)
from travelagent.tools.budget import estimate_transport_cost
from travelagent.tools.geocode import search_nominatim

_OSRM_MODE_ALIASES = {
    "car": "driving",
    "drive": "driving",
    "driving": "driving",
    "taxi": "driving",
}

_WALKING_MAX_DISTANCE_METERS = 5_000
_CLEAR_WIN_MARGIN = 0.18


def estimate_osrm_route(
    origin: str,
    destination: str,
    mode: str,
    config: AppConfig,
) -> RouteEstimate:
    """Estimate fastest route distance and duration through OSRM."""
    # TODO @dkoe00: Add multimodal routing providers.
    normalized_origin = origin.strip()
    normalized_destination = destination.strip()
    normalized_mode = _normalize_mode(mode)

    if not normalized_origin:
        raise ValueError("origin must not be empty.")
    if not normalized_destination:
        raise ValueError("destination must not be empty.")

    origin_candidates = search_nominatim(normalized_origin, config, limit=3).locations
    destination_candidates = search_nominatim(normalized_destination, config, limit=3).locations

    if not origin_candidates:
        raise RuntimeError(f"Could not geocode origin: {normalized_origin!r}.")
    if not destination_candidates:
        raise RuntimeError(f"Could not geocode destination: {normalized_destination!r}.")

    origin_location = origin_candidates[0]
    destination_location = destination_candidates[0]
    payload = _request_osrm_route(
        origin_location,
        destination_location,
        normalized_mode,
        config,
    )

    routes = payload.get("routes")
    if payload.get("code") != "Ok" or not isinstance(routes, list) or not routes:
        message = payload.get("message") or payload.get("code") or "unknown error"
        raise RuntimeError(f"OSRM route estimation failed: {message}.")

    route = routes[0]
    distance_meters = float(route["distance"])
    duration_seconds = float(route["duration"])

    return RouteEstimate(
        origin_query=normalized_origin,
        destination_query=normalized_destination,
        origin=origin_location,
        destination=destination_location,
        mode=normalized_mode,
        distance_meters=distance_meters,
        duration_seconds=duration_seconds,
        duration_minutes=round(duration_seconds / 60, 1),
        uncertainty_notes=_uncertainty_notes(
            origin_candidates,
            destination_candidates,
            normalized_mode,
        ),
    )


def build_estimate_route_tool(config: AppConfig):
    """Build an Agents SDK function tool backed by Nominatim and OSRM."""

    @function_tool
    def estimate_route(
        origin: str,
        destination: str,
        mode: str = "driving",
    ) -> dict[str, Any]:
        """Estimate travel distance and duration between two place names."""
        return estimate_osrm_route(origin, destination, mode, config).model_dump()

    return estimate_route


def compare_transport_options(
    origin: str,
    destination: str,
    config: AppConfig,
    *,
    currency: str = "EUR",
) -> TransportRecommendation:
    """Build and rank practical transportation options for a route."""
    driving_route = estimate_osrm_route(origin, destination, "driving", config)
    options = _build_transport_options(driving_route, currency)
    ranked_options = _rank_options(options)
    selected_options = _select_options(ranked_options)
    recommended_option = ranked_options[0]

    return TransportRecommendation(
        origin_query=driving_route.origin_query,
        destination_query=driving_route.destination_query,
        origin=driving_route.origin,
        destination=driving_route.destination,
        recommended_option=recommended_option,
        options=selected_options,
        summary=_recommendation_summary(recommended_option, selected_options),
        driving_option_included=any(option.mode == "driving" for option in selected_options),
        uncertainty_notes=[
            # TODO @dkoe00: Replace approximate mode comparison.
            "Mode comparison uses driving route data plus heuristic alternatives.",
            *driving_route.uncertainty_notes,
        ],
    )


def build_compare_transport_options_tool(config: AppConfig):
    """Build an Agents SDK tool for ranked transportation options."""

    @function_tool(name_override="compare_transport_options")
    def compare_transport_options_tool(
        origin: str,
        destination: str,
        currency: str = "EUR",
    ) -> dict[str, Any]:
        """Compare practical transportation options between two place names."""
        return compare_transport_options(
            origin,
            destination,
            config,
            currency=currency,
        ).model_dump()

    return compare_transport_options_tool


def _build_transport_options(
    driving_route: RouteEstimate,
    currency: str,
) -> list[TransportOption]:
    options = [
        _option(
            mode="driving",
            label="Drive or rental car",
            route=driving_route,
            distance_meters=driving_route.distance_meters,
            duration_minutes=driving_route.duration_minutes,
            comfort_score=0.76,
            reliability_score=0.74,
            currency=currency,
            ranking_reason="Most flexible option and useful for rental-car decisions.",
            pros=["Direct and flexible.", "Useful if luggage or multi-stop travel matters."],
            cons=["Parking, rental, tolls, and traffic can change the real cost."],
            uncertainty_notes=driving_route.uncertainty_notes,
            include_for_strategic_decision=True,
        ),
        _option(
            mode="taxi",
            label="Taxi",
            route=driving_route,
            distance_meters=driving_route.distance_meters,
            duration_minutes=driving_route.duration_minutes + 5,
            comfort_score=0.82,
            reliability_score=0.66,
            currency=currency,
            ranking_reason="Comfortable door-to-door option with low planning effort.",
            pros=["Door to door.", "Low walking and transfer burden."],
            cons=["Usually more expensive than driving or public transport."],
            uncertainty_notes=[
                "Taxi duration reuses driving route plus a pickup buffer.",
            ],
        ),
        _option(
            mode="rideshare",
            label="Rideshare",
            route=driving_route,
            distance_meters=driving_route.distance_meters,
            duration_minutes=driving_route.duration_minutes + 7,
            comfort_score=0.78,
            reliability_score=0.58,
            currency=currency,
            ranking_reason="Convenient if available, but price and wait time can vary.",
            pros=["Door to door.", "Often convenient in cities."],
            cons=["Surge pricing and availability can vary."],
            uncertainty_notes=[
                "Rideshare duration reuses driving route plus a wait-time buffer.",
            ],
        ),
        _option(
            mode="public_transport",
            label="Public transport",
            route=None,
            distance_meters=driving_route.distance_meters,
            duration_minutes=round(driving_route.duration_minutes * 1.7 + 10, 1),
            comfort_score=0.56,
            reliability_score=0.46,
            currency=currency,
            ranking_reason="Potentially cost-effective, but current estimate is approximate.",
            pros=["Often cheaper than taxi or rideshare.", "Avoids parking."],
            cons=["May involve waiting, transfers, walking, and schedule constraints."],
            uncertainty_notes=[
                # TODO @dkoe00: Integrate public transport routing.
                "Public transport duration is a heuristic placeholder.",
            ],
        ),
    ]

    if driving_route.distance_meters <= _WALKING_MAX_DISTANCE_METERS:
        walking_duration = round((driving_route.distance_meters / 5_000) * 60, 1)
        options.append(
            _option(
                mode="walking",
                label="Walk",
                route=None,
                distance_meters=driving_route.distance_meters,
                duration_minutes=walking_duration,
                comfort_score=0.66 if driving_route.distance_meters <= 2_500 else 0.44,
                reliability_score=0.86,
                currency=currency,
                ranking_reason="Free and predictable when the distance is manageable.",
                pros=["No direct cost.", "Predictable and avoids traffic."],
                cons=["Can be tiring with luggage, bad weather, or time pressure."],
                uncertainty_notes=[
                    # TODO @dkoe00: Add pedestrian routing.
                    "Walking uses road-route distance as an approximation.",
                ],
            )
        )

    return options


def _option(
    *,
    mode: TransportMode,
    label: str,
    route: RouteEstimate | None,
    distance_meters: float,
    duration_minutes: float,
    comfort_score: float,
    reliability_score: float,
    currency: str,
    ranking_reason: str,
    pros: list[str],
    cons: list[str],
    uncertainty_notes: list[str],
    include_for_strategic_decision: bool = False,
) -> TransportOption:
    # TODO @dkoe00: Route cost estimates through Budget Agent.
    cost_estimate = estimate_transport_cost(
        mode,
        distance_meters,
        duration_minutes,
        currency,
    )
    return TransportOption(
        mode=mode,
        label=label,
        route=route,
        distance_meters=distance_meters,
        duration_minutes=duration_minutes,
        comfort_score=comfort_score,
        reliability_score=reliability_score,
        cost_estimate=cost_estimate,
        ranking_reason=ranking_reason,
        pros=pros,
        cons=cons,
        uncertainty_notes=uncertainty_notes + cost_estimate.assumptions,
        include_for_strategic_decision=include_for_strategic_decision,
    )


def _rank_options(options: list[TransportOption]) -> list[TransportOption]:
    fastest = min(option.duration_minutes for option in options)
    cheapest = min(_cost_amount(option.cost_estimate) for option in options)

    scored_options: list[TransportOption] = []
    for option in options:
        time_score = _ratio_score(fastest, option.duration_minutes)
        cost_score = _ratio_score(cheapest, _cost_amount(option.cost_estimate))
        comfort_score = option.comfort_score
        reliability_score = option.reliability_score
        overall = (
            time_score * 0.35
            + cost_score * 0.25
            + comfort_score * 0.25
            + reliability_score * 0.15
        )
        scored_options.append(
            option.model_copy(
                update={
                    "score": TransportOptionScore(
                        overall=round(overall, 3),
                        time=round(time_score, 3),
                        cost=round(cost_score, 3),
                        comfort=round(comfort_score, 3),
                        reliability=round(reliability_score, 3),
                    )
                }
            )
        )

    return sorted(
        scored_options,
        key=lambda option: option.score.overall if option.score else 0,
        reverse=True,
    )


def _select_options(ranked_options: list[TransportOption]) -> list[TransportOption]:
    best = ranked_options[0]
    second = ranked_options[1] if len(ranked_options) > 1 else None
    best_score = best.score.overall if best.score else 0
    second_score = second.score.overall if second and second.score else 0

    if best.mode == "driving" and best_score - second_score >= _CLEAR_WIN_MARGIN:
        return [best]

    selected = ranked_options[:3]
    if not any(option.mode == "driving" for option in selected):
        driving_option = next(option for option in ranked_options if option.mode == "driving")
        selected[-1] = driving_option
    walking_option = next(
        (option for option in ranked_options if option.mode == "walking"),
        None,
    )
    if walking_option is not None and not any(option.mode == "walking" for option in selected):
        replace_index = 1 if selected[-1].mode == "driving" else -1
        selected[replace_index] = walking_option
    return selected


def _recommendation_summary(
    recommended_option: TransportOption,
    selected_options: list[TransportOption],
) -> str:
    if len(selected_options) == 1:
        return f"{recommended_option.label} is clearly the strongest current option."
    return (
        f"{recommended_option.label} ranks best, but the selected options have "
        "different time, comfort, and cost tradeoffs."
    )


def _cost_amount(cost_estimate: TransportCostEstimate | None) -> float:
    if cost_estimate is None:
        return 0
    return cost_estimate.estimated_cost.amount


def _ratio_score(best_value: float, current_value: float) -> float:
    if current_value <= 0:
        return 1
    if best_value <= 0:
        return 1
    return max(0, min(best_value / current_value, 1))


def _request_osrm_route(
    origin: Geolocation,
    destination: Geolocation,
    mode: str,
    config: AppConfig,
) -> dict[str, Any]:
    coordinates = (
        f"{origin.longitude},{origin.latitude};"
        f"{destination.longitude},{destination.latitude}"
    )
    params = urlencode({"overview": "false", "alternatives": "false", "steps": "false"})
    request = Request(
        f"{config.osrm_base_url}/{mode}/{coordinates}?{params}",
        headers={"Accept": "application/json"},
    )

    try:
        with urlopen(request, timeout=config.osrm_timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"OSRM route estimation failed with HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"OSRM route estimation failed: {exc.reason}.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("OSRM returned invalid JSON.") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("OSRM returned an unexpected response shape.")

    return payload


def _normalize_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized in _OSRM_MODE_ALIASES:
        return _OSRM_MODE_ALIASES[normalized]

    supported = ", ".join(sorted(_OSRM_MODE_ALIASES))
    raise ValueError(
        f"Unsupported route mode {mode!r}. Supported aliases for now: {supported}."
    )


def _uncertainty_notes(
    origin_candidates: list[Geolocation],
    destination_candidates: list[Geolocation],
    mode: str,
) -> list[str]:
    notes = [
        # TODO @dkoe00: Replace driving-only uncertainty note.
        f"Mode {mode!r} estimates road travel only; public transport is not included yet.",
    ]
    if len(origin_candidates) > 1:
        notes.append("Origin geocoding returned multiple candidates; first result was used.")
    if len(destination_candidates) > 1:
        notes.append("Destination geocoding returned multiple candidates; first result was used.")
    return notes
