from typing import Any

from agents import Agent, AgentHookContext, RunContextWrapper, RunHooks, Tool
from agents.items import TResponseInputItem

_LABELS = {
    "de": {
        "agent": "→ {name} arbeitet …",
        "tool_start": "   🔧 {tool} …",
        "tool_end": "   ✓ {tool}",
        "llm_start": "   🤖 {name} denkt nach …",
    },
    "en": {
        "agent": "→ {name} working …",
        "tool_start": "   🔧 {tool} …",
        "tool_end": "   ✓ {tool}",
        "llm_start": "   🤖 {name} thinking …",
    },
}


class ProgressHooks(RunHooks):
    """Prints live progress (agent handoffs, tool calls) while a run is in flight.

    Without this, a run that makes several sequential tool calls (e.g. the Places Agent
    calling search_activities multiple times) produces no output at all until it finishes.
    """

    def __init__(self, language: str = "de") -> None:
        self._labels = _LABELS.get(language, _LABELS["de"])

    async def on_agent_start(self, context: AgentHookContext[Any], agent: Agent[Any]) -> None:
        print(self._labels["agent"].format(name=agent.name))

    async def on_llm_start(
        self,
        context: RunContextWrapper[Any],
        agent: Agent[Any],
        system_prompt: str | None,
        input_items: list[TResponseInputItem],
    ) -> None:
        print(self._labels["llm_start"].format(name=agent.name))

    async def on_tool_start(self, context: RunContextWrapper[Any], agent: Agent[Any], tool: Tool) -> None:
        print(self._labels["tool_start"].format(tool=tool.name))

    async def on_tool_end(
        self, context: RunContextWrapper[Any], agent: Agent[Any], tool: Tool, result: object
    ) -> None:
        print(self._labels["tool_end"].format(tool=tool.name))
