"""In-memory session store. Single-process prototype — no persistence, no locking
beyond a per-session asyncio lock to serialize runs within one conversation."""

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any

from agents import Agent

from travelagent.agents.coordinator import build_coordinator_agent
from travelagent.config import APP_CONFIG


@dataclass
class ChatSession:
    session_id: str
    agent: Agent
    history: list[dict[str, Any]] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


_SESSIONS: dict[str, ChatSession] = {}


def create_session() -> ChatSession:
    session_id = uuid.uuid4().hex
    session = ChatSession(session_id=session_id, agent=build_coordinator_agent(APP_CONFIG))
    _SESSIONS[session_id] = session
    return session


def get_session(session_id: str) -> ChatSession | None:
    return _SESSIONS.get(session_id)


def delete_session(session_id: str) -> None:
    _SESSIONS.pop(session_id, None)
