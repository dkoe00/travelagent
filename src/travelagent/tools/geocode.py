"""Geocoding tools for the Transportation Agent."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agents import function_tool

from travelagent.config import AppConfig
from travelagent.schemas.transportation import Geolocation, GeolocationList


def search_nominatim(
    query: str,
    config: AppConfig,
    *,
    limit: int = 5,
) -> GeolocationList:
    """Search Nominatim and return normalized geocoding candidates."""
    normalized_query = query.strip()
    if not normalized_query:
        return GeolocationList(query=query, locations=[])

    safe_limit = max(1, min(limit, 10))
    params: dict[str, str | int] = {
        "q": normalized_query,
        "format": "jsonv2",
        "addressdetails": 1,
        "limit": safe_limit,
    }
    if config.nominatim_email:
        params["email"] = config.nominatim_email

    request = Request(
        f"{config.nominatim_base_url}?{urlencode(params)}",
        headers={
            "Accept": "application/json",
            "User-Agent": config.nominatim_user_agent,
        },
    )

    try:
        with urlopen(request, timeout=config.nominatim_timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Nominatim geocoding failed with HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"Nominatim geocoding failed: {exc.reason}.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Nominatim returned invalid JSON.") from exc

    if not isinstance(payload, list):
        raise RuntimeError("Nominatim returned an unexpected response shape.")

    locations: list[Geolocation] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        location = _to_geolocation(item)
        if location is not None:
            locations.append(location)

    return GeolocationList(query=normalized_query, locations=locations)


def build_geocode_location_tool(config: AppConfig):
    """Build an Agents SDK function tool backed by Nominatim search."""

    @function_tool
    def geocode_location(query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Geocode a location name or address into latitude/longitude candidates."""
        result = search_nominatim(query, config, limit=limit)
        return [location.model_dump() for location in result.locations]

    return geocode_location


def _to_geolocation(item: dict[str, Any]) -> Geolocation | None:
    try:
        latitude = float(item["lat"])
        longitude = float(item["lon"])
    except (KeyError, TypeError, ValueError):
        return None

    return Geolocation(
        display_name=str(item.get("display_name") or ""),
        latitude=latitude,
        longitude=longitude,
        category=_optional_str(item.get("category") or item.get("class")),
        kind=_optional_str(item.get("type") or item.get("addresstype")),
        importance=_optional_float(item.get("importance")),
    )


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
