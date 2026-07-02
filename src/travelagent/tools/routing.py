"""Routing tools for the Transportation Agent."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agents import function_tool

from travelagent.config import AppConfig
from travelagent.schemas.transportation import Geolocation, RouteEstimate
from travelagent.tools.geocode import search_nominatim

_OSRM_MODE_ALIASES = {
    "car": "driving",
    "drive": "driving",
    "driving": "driving",
    "taxi": "driving",
}


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
