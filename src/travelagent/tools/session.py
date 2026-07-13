"""Session lifecycle tools for final pipeline stages."""

from __future__ import annotations

from agents import RunContextWrapper, function_tool

from travelagent.session_state import PlanningSessionState


@function_tool
def finish_planning(context: RunContextWrapper[PlanningSessionState]) -> str:
    """Mark the current planning session as complete."""
    context.context.should_exit = True
    return "Planning session completed."
