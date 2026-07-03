"""Budget tools for cost estimation."""

from __future__ import annotations

from typing import Any

from agents import function_tool

from travelagent.schemas.budget import CostRange, MoneyEstimate, TransportCostEstimate

_TRANSPORT_MODE_ALIASES = {
    "walk": "walking",
    "walking": "walking",
    "car": "driving",
    "drive": "driving",
    "driving": "driving",
    "rental_car": "driving",
    "rental car": "driving",
    "taxi": "taxi",
    "rideshare": "rideshare",
    "uber": "rideshare",
    "public": "public_transport",
    "public_transport": "public_transport",
    "public transport": "public_transport",
    "transit": "public_transport",
}


def estimate_transport_cost(
    mode: str,
    distance_meters: float,
    duration_minutes: float,
    currency: str = "EUR",
) -> TransportCostEstimate:
    """Estimate transportation cost from mode, distance, and duration."""
    # TODO @dkoe00: Replace heuristic fares with live prices.
    normalized_mode = _normalize_transport_mode(mode)
    normalized_currency = currency.strip().upper() or "EUR"
    distance_km = max(distance_meters, 0) / 1000
    safe_duration = max(duration_minutes, 0)

    if normalized_mode == "walking":
        return _build_estimate(
            mode=normalized_mode,
            distance_meters=distance_meters,
            duration_minutes=safe_duration,
            currency=normalized_currency,
            amount=0,
            min_amount=0,
            max_amount=0,
            confidence="high",
            assumptions=["Walking has no direct transportation fare."],
        )

    if normalized_mode == "driving":
        amount = distance_km * 0.18
        return _build_estimate(
            mode=normalized_mode,
            distance_meters=distance_meters,
            duration_minutes=safe_duration,
            currency=normalized_currency,
            amount=amount,
            min_amount=distance_km * 0.12,
            max_amount=distance_km * 0.35,
            confidence="medium",
            assumptions=[
                "Driving estimate covers approximate fuel or energy cost only.",
                "Rental, parking, tolls, insurance, and deposits are not included.",
            ],
        )

    if normalized_mode == "taxi":
        amount = 4.0 + distance_km * 2.2 + safe_duration * 0.35
        return _build_estimate(
            mode=normalized_mode,
            distance_meters=distance_meters,
            duration_minutes=safe_duration,
            currency=normalized_currency,
            amount=amount,
            min_amount=amount * 0.75,
            max_amount=amount * 1.45,
            confidence="low",
            assumptions=[
                "Taxi estimate uses a generic urban fare formula.",
                "Local tariffs, surge pricing, airport fees, and tips are not included.",
            ],
        )

    if normalized_mode == "rideshare":
        amount = 3.5 + distance_km * 1.9 + safe_duration * 0.3
        return _build_estimate(
            mode=normalized_mode,
            distance_meters=distance_meters,
            duration_minutes=safe_duration,
            currency=normalized_currency,
            amount=amount,
            min_amount=amount * 0.7,
            max_amount=amount * 1.8,
            confidence="low",
            assumptions=[
                "Rideshare estimate uses a generic fare formula.",
                "Availability and surge pricing can change substantially.",
            ],
        )

    if normalized_mode == "public_transport":
        amount = 3.0 if distance_km <= 15 else 6.0
        return _build_estimate(
            mode=normalized_mode,
            distance_meters=distance_meters,
            duration_minutes=safe_duration,
            currency=normalized_currency,
            amount=amount,
            min_amount=max(amount - 1.5, 0),
            max_amount=amount + 4.0,
            confidence="low",
            assumptions=[
                "Public transport estimate uses a generic local/regional fare range.",
                "Actual fares depend on city, zones, passes, and operator rules.",
            ],
        )

    raise ValueError(f"Unsupported transport mode: {mode!r}.")


def build_estimate_transport_cost_tool():
    """Build an Agents SDK function tool for transportation cost estimates."""

    @function_tool(name_override="estimate_transport_cost")
    def estimate_transport_cost_tool(
        mode: str,
        distance_meters: float,
        duration_minutes: float,
        currency: str = "EUR",
    ) -> dict[str, Any]:
        """Estimate the cost of one transportation option."""
        return estimate_transport_cost(
            mode,
            distance_meters,
            duration_minutes,
            currency,
        ).model_dump()

    return estimate_transport_cost_tool


def _normalize_transport_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized in _TRANSPORT_MODE_ALIASES:
        return _TRANSPORT_MODE_ALIASES[normalized]

    supported = ", ".join(sorted(_TRANSPORT_MODE_ALIASES))
    raise ValueError(
        f"Unsupported transport mode {mode!r}. Supported aliases for now: {supported}."
    )


def _build_estimate(
    *,
    mode: str,
    distance_meters: float,
    duration_minutes: float,
    currency: str,
    amount: float,
    min_amount: float,
    max_amount: float,
    confidence: str,
    assumptions: list[str],
) -> TransportCostEstimate:
    return TransportCostEstimate(
        mode=mode,
        distance_meters=max(distance_meters, 0),
        duration_minutes=duration_minutes,
        estimated_cost=MoneyEstimate(
            amount=round(max(amount, 0), 2),
            currency=currency,
        ),
        estimated_range=CostRange(
            min=MoneyEstimate(amount=round(max(min_amount, 0), 2), currency=currency),
            max=MoneyEstimate(amount=round(max(max_amount, 0), 2), currency=currency),
        ),
        confidence=confidence,
        assumptions=assumptions,
    )
