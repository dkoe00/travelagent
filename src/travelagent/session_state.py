"""Mutable per-conversation state shared with SDK tools."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlanningSessionState:
    """Runtime flags controlled by tools during one planning session."""

    should_exit: bool = False
