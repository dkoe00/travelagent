"""Translates openai-agents stream events into the SSE vocabulary the frontend consumes.

SSE event vocabulary (event name → JSON data payload):
  text_delta     {"delta": str}                        streamed coordinator text
  tool_started   {"tool": str, "arguments": str}       coordinator called a specialist tool
  tool_finished  {"tool": str, "payload": Any}         specialist tool returned (payload = parsed JSON or {"text": str})
  constraints    {"region": ..., ...}                  update_constraints tool call (Phase D)
  final          {"text": str}                         coordinator's final synthesized message
  error          {"message": str}
  done           {}                                    always the last event
"""

import json
from collections.abc import AsyncIterator
from typing import Any

from agents.result import RunResultStreaming

SPECIALIST_TOOLS = {"discover_destinations", "find_places", "plan_itinerary"}
CONSTRAINTS_TOOL = "update_constraints"


def sse_format(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _get(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _parse_json_or_text(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return {"text": value}
    # Pydantic model — convert to dict
    if hasattr(value, "model_dump"):
        return value.model_dump()
    # Already a dict or other JSON-serializable type
    return value


async def translate_stream(result: RunResultStreaming) -> AsyncIterator[str]:
    call_id_to_tool: dict[str, str] = {}
    try:
        async for event in result.stream_events():
            match event.type:
                case "raw_response_event":
                    if getattr(event.data, "type", "") == "response.output_text.delta":
                        yield sse_format("text_delta", {"delta": event.data.delta})
                case "run_item_stream_event":
                    match event.name:
                        case "tool_called":
                            raw = event.item.raw_item
                            tool = _get(raw, "name") or ""
                            call_id = _get(raw, "call_id") or ""
                            arguments = _get(raw, "arguments") or ""
                            call_id_to_tool[call_id] = tool
                            if tool == CONSTRAINTS_TOOL:
                                yield sse_format("constraints", _parse_json_or_text(arguments))
                            elif tool in SPECIALIST_TOOLS:
                                yield sse_format("tool_started", {"tool": tool, "arguments": arguments})
                        case "tool_output":
                            call_id = _get(event.item.raw_item, "call_id") or ""
                            tool = call_id_to_tool.get(call_id, "")
                            if tool in SPECIALIST_TOOLS:
                                payload = _parse_json_or_text(event.item.output)
                                yield sse_format("tool_finished", {"tool": tool, "payload": payload})
        final_text = result.final_output if isinstance(result.final_output, str) else str(result.final_output)
        yield sse_format("final", {"text": final_text})
    except Exception as exc:  # surface run failures to the client instead of a dead stream
        yield sse_format("error", {"message": str(exc)})
    yield sse_format("done", {})
