"""Runtime setup for connecting app configuration to the Agents SDK."""

from __future__ import annotations

import agents
from openai import AsyncOpenAI

from travelagent.config import AppConfig


def configure_agents_sdk(config: AppConfig) -> None:
    """Configure the OpenAI Agents SDK from application settings."""
    if config.llm_api_key:
        agents.set_default_openai_key(
            config.llm_api_key,
            use_for_tracing=config.enable_tracing,
        )

    if config.llm_base_url:
        custom_client = AsyncOpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url,
        )
        agents.set_default_openai_client(
            custom_client,
            use_for_tracing=config.enable_tracing,
        )
