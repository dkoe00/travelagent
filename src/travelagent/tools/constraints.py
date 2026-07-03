from agents import function_tool


@function_tool
def update_constraints(
    region: str | None = None,
    activity: str | None = None,
    duration_days: int | None = None,
    month: str | None = None,
    budget: str | None = None,
) -> dict[str, str | int | None]:
    """Report the travel constraints extracted from the conversation so far.

    Call this whenever a constraint is newly learned or changes. Pass only the
    fields you know; omit unknown ones. This tool only records state for the UI —
    it returns the same values back and has no other effect.
    """
    values = {
        "region": region,
        "activity": activity,
        "duration_days": duration_days,
        "month": month,
        "budget": budget,
    }
    return {key: value for key, value in values.items() if value is not None}
