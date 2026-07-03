---
project_name: 'travelagent'
user_name: 'Paul'
date: '2026-07-02'
sections_completed: ['technology_stack', 'language_specific_rules', 'framework_specific_rules', 'testing_rules', 'code_quality_style_rules', 'development_workflow_rules', 'critical_dont_miss_rules']
existing_patterns_found: 8
status: 'complete'
rule_count: 49
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- Python `>=3.13` is the runtime target from `pyproject.toml`.
- Dependency and environment management use `uv`; prefer `uv sync` and `uv run ...` over direct `pip`/`python` assumptions.
- Package layout uses setuptools with `src/` as the package root; import app code as `travelagent.*`.
- Core dependencies:
  - `openai-agents>=0.17.6`
  - `pydantic>=2.13.4`
  - `python-dotenv>=1.2.2`
  - `asyncio>=4.0.0`
- Build backend is `setuptools.build_meta` with `setuptools>=61`.
- Runtime LLM configuration comes from environment variables loaded via `python-dotenv`: `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, and `ENABLE_TRACING`.
- Default model is `gpt-5-nano` when `LLM_MODEL` is unset or empty.

## Critical Implementation Rules

### Language-Specific Rules

- Keep application code under `src/travelagent/`; do not add top-level Python packages outside the existing `src/` layout.
- Use absolute imports from `travelagent.*` for project modules, matching the current package layout.
- Keep `from __future__ import annotations` in non-trivial modules that define typed functions, dataclasses, or SDK-facing builders.
- Configuration values should flow through `AppConfig` in `travelagent.config`; avoid reading environment variables directly inside agents or tools.
- Treat empty environment variable strings as missing values, following the existing `_empty_to_none` behavior.
- Preserve strict boolean parsing for `ENABLE_TRACING`; invalid values should fail loudly instead of silently defaulting.
- Keep secrets out of repr/log output; `AppConfig.llm_api_key` is intentionally declared with `repr=False`.

### Framework-Specific Rules

- Configure the OpenAI Agents SDK only through `configure_agents_sdk(config)` in `travelagent.runtime` before running agents.
- Support both default OpenAI configuration and custom OpenAI-compatible endpoints via `LLM_BASE_URL`.
- When `LLM_BASE_URL` is set, create an `AsyncOpenAI` client and pass it to `agents.set_default_openai_client`.
- Pass `use_for_tracing=config.enable_tracing` consistently when setting the SDK key or client.
- Agent construction should live in `src/travelagent/agents/<role>.py` as `build_<role>_agent(config)` functions.
- Agent model selection should come from `config.llm_model`; do not hard-code model names inside individual agents.
- The current coordinator is terminal-only and intentionally has `Do not use tools.` in its instructions until tool wiring is implemented.
- Specialist agents are planned but mostly placeholders; add behavior incrementally instead of inventing unused orchestration layers.

### Testing Rules

- Do not assume a test framework is already configured; add one explicitly before adding test files that require it.
- Prefer tests around deterministic code first: config parsing, environment defaults, boolean parsing, schema validation, tool wrappers, and fallback data behavior.
- Avoid live LLM/API calls in automated tests unless they are clearly marked as integration or smoke tests.
- Use fake SDK-facing inputs, API wrapper boundaries, and fallback data for repeatable tests; keep network-dependent checks out of the default test path.
- When testing agent construction, verify configuration wiring and instructions without requiring a real model call.
- Keep seminar/demo smoke tests separate from deterministic unit tests so prototype validation does not depend on external service availability.

### Code Quality & Style Rules

- There is no committed formatter/linter configuration yet; do not invent style-only churn unrelated to the current task.
- Keep modules small and role-focused: config in `config.py`, SDK setup in `runtime.py`, agent builders in `agents/`, schemas in `schemas/`, tools in `tools/`.
- Name agent modules by role using lowercase filenames, e.g. `coordinator.py`, `packing.py`, `transportation.py`.
- Name agent factory functions as `build_<role>_agent(config)`.
- Keep user-facing prototype code in `main.py`; avoid mixing CLI/demo behavior into reusable package modules.
- Use concise module docstrings to mark placeholders or responsibilities, matching the current code style.
- Do not add broad abstractions until specialist agents, schemas, or tools actually need shared behavior.

### Development Workflow Rules

- Use `uv sync` to install dependencies and `uv run ...` to execute project commands.
- Run the current prototype with `uv run python main.py`.
- Keep local secrets in `.env`; update `.env.example` when adding required configuration variables.
- Do not commit `.env` or real API keys.
- No branch naming, commit message, PR, CI, or deployment conventions are defined in the repository yet; do not fabricate them in implementation guidance.
- Treat the project as a private travel planning tool that began as a university seminar prototype: optimize near-term changes for clarity and demonstrability while preserving a path to practical real-world use.

### Critical Don't-Miss Rules

- Do not bypass `configure_agents_sdk`; otherwise custom `LLM_BASE_URL`, tracing, and API key behavior may silently diverge from the prototype.
- Do not hard-code API keys, base URLs, or model names in agent modules, tools, schemas, or `main.py`.
- Do not make automated tests depend on live LLM responses or live external APIs; use deterministic seams around configuration, schema validation, tool wrappers, and fallback data.
- Do not wire tools into the Coordinator Agent without also updating its instructions; it currently explicitly says `Do not use tools.`
- Do not replace the planned multi-agent architecture with a single large agent unless the README and project context are intentionally updated.
- Do not add fragile travel-data integrations without stable tool interfaces, schema boundaries, fallback behavior for unavailable APIs, and concise `TODO @dkoe00:` comments where MVP shortcuts must later be replaced.
- Do not log full environment-derived configuration objects if secrets may be present.
- Do not treat placeholder modules as dead code; they mark intended project boundaries for upcoming specialist agents, schemas, and tools.

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code.
- Follow all rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new durable project patterns emerge.

**For Humans:**

- Keep this file lean and focused on agent needs.
- Update it when the technology stack changes.
- Review periodically for outdated rules.
- Remove rules that become obvious over time.

Last Updated: 2026-07-02
