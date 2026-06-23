"""Runtime configuration for the Travel Planning Assistant."""

from __future__ import annotations

from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()

_TRUE_VALUES = {"1", "true", "t", "yes", "y", "on"}
_FALSE_VALUES = {"0", "false", "f", "no", "n", "off"}


def _empty_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _parse_bool(value: str | None, default: bool = False) -> bool:
    normalized = _empty_to_none(value)
    if normalized is None:
        return default

    lowered = normalized.lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean value for ENABLE_TRACING: {value!r}. "
        "Expected one of 1/0, true/false, yes/no, on/off."
    )


@dataclass(frozen=True)
class AppConfig:
    llm_api_key: str | None = field(repr=False)
    llm_base_url: str | None
    llm_model: str = "gpt-5-nano"
    enable_tracing: bool = False


APP_CONFIG = AppConfig(
    llm_api_key=_empty_to_none(os.getenv("LLM_API_KEY")),
    llm_base_url=_empty_to_none(os.getenv("LLM_BASE_URL")),
    llm_model=_empty_to_none(os.getenv("LLM_MODEL")) or "gpt-5-nano",
    enable_tracing=_parse_bool(os.getenv("ENABLE_TRACING"), default=False),
)
